"""Bronze and Silver transformations for vehicle telemetry."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession, functions as F
from pyspark.sql.types import StructType

from spark.utils.config_loader import DataQualitySettings, KafkaSettings
from spark.utils.quality_rules import apply_quality_rules
from spark.utils.schemas import SILVER_COLUMNS, TELEMETRY_PARSE_SCHEMA, TELEMETRY_SCHEMA


def read_kafka_stream(spark: SparkSession, kafka: KafkaSettings) -> DataFrame:
    """Create a streaming DataFrame from the telemetry Kafka topic."""
    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka.bootstrap_servers)
        .option("subscribe", kafka.telemetry_topic)
        .option("startingOffsets", kafka.starting_offsets)
        .option("failOnDataLoss", str(kafka.fail_on_data_loss).lower())
        .load()
    )


def read_parquet_stream(
    spark: SparkSession,
    path: str,
    schema: StructType | None = None,
) -> DataFrame:
    """Create a streaming DataFrame from a Parquet path."""
    _ensure_local_directory(path)
    reader = spark.readStream.format("parquet")
    if schema is not None:
        reader = reader.schema(schema)
    return reader.load(path)


def build_bronze_dataframe(kafka_df: DataFrame) -> DataFrame:
    """Parse Kafka value payloads into a Bronze telemetry dataframe."""
    raw_payload = F.col("value").cast("string")
    base_df = kafka_df.select(
        raw_payload.alias("raw_payload"),
        _optional_column(kafka_df, "topic", "string").alias("source_topic"),
        _optional_column(kafka_df, "partition", "int").alias("source_partition"),
        _optional_column(kafka_df, "offset", "long").alias("source_offset"),
        _optional_column(kafka_df, "timestamp", "timestamp").alias("kafka_timestamp"),
    ).withColumn(
        "parsed_payload",
        F.from_json(
            F.col("raw_payload"),
            TELEMETRY_PARSE_SCHEMA,
            {"mode": "PERMISSIVE", "columnNameOfCorruptRecord": "_corrupt_record"},
        ),
    )

    parsed_columns = [
        F.col(f"parsed_payload.{field.name}").alias(field.name)
        for field in TELEMETRY_SCHEMA.fields
    ]

    return (
        base_df.select(
            "raw_payload",
            "source_topic",
            "source_partition",
            "source_offset",
            "kafka_timestamp",
            "parsed_payload",
            *parsed_columns,
        )
        .withColumn("ingest_timestamp", F.current_timestamp())
        .withColumn("event_timestamp", F.to_timestamp(F.col("timestamp")))
        .withColumn(
            "event_date",
            F.coalesce(F.to_date("event_timestamp"), F.to_date("ingest_timestamp")),
        )
        .withColumn(
            "parse_error",
            F.col("raw_payload").isNotNull()
            & F.col("parsed_payload._corrupt_record").isNotNull(),
        )
        .withColumn(
            "record_id",
            F.sha2(
                F.concat_ws(
                    "||",
                    F.coalesce(F.col("source_topic"), F.lit("")),
                    F.coalesce(F.col("source_partition").cast("string"), F.lit("")),
                    F.coalesce(F.col("source_offset").cast("string"), F.lit("")),
                    F.coalesce(F.col("raw_payload"), F.lit("")),
                ),
                256,
            ),
        )
        .drop("parsed_payload")
    )


def build_silver_dataframe(
    bronze_df: DataFrame,
    quality: DataQualitySettings,
    watermark_delay: str | None = None,
) -> DataFrame:
    """Build a clean, deduplicated Silver dataframe from Bronze records."""
    standardized_df = standardize_silver_records(bronze_df)
    quality_df = apply_quality_rules(standardized_df, quality)
    valid_df = quality_df.filter(F.col("is_valid"))
    deduplicated_df = deduplicate_silver_records(valid_df, watermark_delay)
    return deduplicated_df.select(*SILVER_COLUMNS)


def standardize_silver_records(bronze_df: DataFrame) -> DataFrame:
    """Normalize types, casing, and nullable defaults for Silver telemetry."""
    clean_df = bronze_df.filter(~F.coalesce(F.col("parse_error"), F.lit(False)))

    return (
        clean_df.withColumn("vehicle_id", F.upper(F.trim(F.col("vehicle_id"))))
        .withColumn("model", F.trim(F.col("model")))
        .withColumn(
            "event_timestamp",
            F.coalesce(F.col("event_timestamp"), F.to_timestamp(F.col("timestamp"))),
        )
        .withColumn("event_date", F.to_date(F.col("event_timestamp")))
        .withColumn("speed", F.col("speed").cast("double"))
        .withColumn("rpm", F.col("rpm").cast("int"))
        .withColumn("engine_temp", F.col("engine_temp").cast("double"))
        .withColumn(
            "battery_level",
            F.coalesce(F.col("battery_level"), F.col("battery")).cast("double"),
        )
        .withColumn("fuel", F.col("fuel").cast("double"))
        .withColumn("latitude", F.col("latitude").cast("double"))
        .withColumn("longitude", F.col("longitude").cast("double"))
        .withColumn(
            "fault_code",
            F.upper(F.trim(F.coalesce(F.col("fault_code"), F.lit("NONE")))),
        )
        .withColumn(
            "severity",
            F.upper(F.trim(F.coalesce(F.col("severity"), F.lit("NONE")))),
        )
        .withColumn(
            "weather",
            F.initcap(F.trim(F.coalesce(F.col("weather"), F.lit("UNKNOWN")))),
        )
        .withColumn("outside_temperature", F.col("outside_temperature").cast("double"))
        .withColumn("last_service_days", F.col("last_service_days").cast("int"))
        .withColumn(
            "service_type",
            F.initcap(F.trim(F.coalesce(F.col("service_type"), F.lit("UNKNOWN")))),
        )
    )


def deduplicate_silver_records(
    dataframe: DataFrame,
    watermark_delay: str | None = None,
) -> DataFrame:
    """Drop duplicate vehicle events by natural event key."""
    dedupe_df = dataframe
    if watermark_delay and dataframe.isStreaming:
        dedupe_df = dedupe_df.withWatermark("event_timestamp", watermark_delay)
    return dedupe_df.dropDuplicates(["vehicle_id", "event_timestamp"])


def write_stream_to_parquet(
    dataframe: DataFrame,
    output_path: str,
    checkpoint_path: str,
    partition_columns: Iterable[str],
    trigger_processing_time: str,
    output_mode: str,
    once: bool = False,
):
    """Write a streaming DataFrame to Parquet with checkpointing."""
    _ensure_local_directory(output_path)
    _ensure_local_directory(checkpoint_path)

    writer = (
        dataframe.writeStream.format("parquet")
        .outputMode(output_mode)
        .option("path", output_path)
        .option("checkpointLocation", checkpoint_path)
    )

    partition_columns_tuple = tuple(partition_columns)
    if partition_columns_tuple:
        writer = writer.partitionBy(*partition_columns_tuple)

    if once:
        writer = writer.trigger(availableNow=True)
    else:
        writer = writer.trigger(processingTime=trigger_processing_time)

    return writer.start()


def _optional_column(dataframe: DataFrame, column_name: str, data_type: str):
    if column_name in dataframe.columns:
        return F.col(column_name).cast(data_type)
    return F.lit(None).cast(data_type)


def _ensure_local_directory(path: str) -> None:
    if "://" in path:
        return
    Path(path).mkdir(parents=True, exist_ok=True)
