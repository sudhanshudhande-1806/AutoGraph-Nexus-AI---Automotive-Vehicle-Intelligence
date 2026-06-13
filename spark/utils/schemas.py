"""Spark schemas for vehicle telemetry."""

from __future__ import annotations

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

TELEMETRY_SCHEMA = StructType(
    [
        StructField("vehicle_id", StringType(), True),
        StructField("model", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("rpm", IntegerType(), True),
        StructField("engine_temp", DoubleType(), True),
        StructField("battery_level", DoubleType(), True),
        StructField("battery", DoubleType(), True),
        StructField("fuel", DoubleType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("fault_code", StringType(), True),
        StructField("severity", StringType(), True),
        StructField("weather", StringType(), True),
        StructField("outside_temperature", DoubleType(), True),
        StructField("last_service_days", IntegerType(), True),
        StructField("service_type", StringType(), True),
    ]
)

TELEMETRY_PARSE_SCHEMA = StructType(
    [
        *TELEMETRY_SCHEMA.fields,
        StructField("_corrupt_record", StringType(), True),
    ]
)

BRONZE_SCHEMA = StructType(
    [
        StructField("raw_payload", StringType(), True),
        StructField("source_topic", StringType(), True),
        StructField("source_partition", IntegerType(), True),
        StructField("source_offset", LongType(), True),
        StructField("kafka_timestamp", TimestampType(), True),
        *TELEMETRY_SCHEMA.fields,
        StructField("ingest_timestamp", TimestampType(), True),
        StructField("event_timestamp", TimestampType(), True),
        StructField("event_date", DateType(), True),
        StructField("parse_error", BooleanType(), True),
        StructField("record_id", StringType(), True),
    ]
)

SILVER_COLUMNS = (
    "vehicle_id",
    "event_timestamp",
    "event_date",
    "model",
    "speed",
    "rpm",
    "engine_temp",
    "battery_level",
    "fuel",
    "latitude",
    "longitude",
    "fault_code",
    "severity",
    "weather",
    "outside_temperature",
    "last_service_days",
    "service_type",
    "source_topic",
    "source_partition",
    "source_offset",
    "record_id",
    "ingest_timestamp",
    "quality_errors",
    "is_valid",
)
