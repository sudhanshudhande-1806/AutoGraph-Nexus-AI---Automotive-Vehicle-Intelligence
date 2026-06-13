"""Reusable data quality rules for Silver telemetry."""

from __future__ import annotations

from pyspark.sql import DataFrame, functions as F

from spark.utils.config_loader import DataQualitySettings


def apply_quality_rules(
    dataframe: DataFrame,
    quality: DataQualitySettings,
) -> DataFrame:
    """Attach quality_errors and is_valid columns to a standardized dataframe."""
    valid_fault_codes = [code.upper() for code in quality.valid_fault_codes]

    error_columns = [
        F.when(
            F.col("vehicle_id").isNull() | (F.length(F.col("vehicle_id")) == 0),
            F.lit("vehicle_id_missing"),
        ),
        F.when(F.col("event_timestamp").isNull(), F.lit("event_timestamp_missing")),
        F.when(F.col("speed").isNull(), F.lit("speed_missing")),
        F.when(
            F.col("speed").isNotNull()
            & (
                (F.col("speed") < F.lit(quality.min_speed))
                | (F.col("speed") > F.lit(quality.max_speed))
            ),
            F.lit("speed_out_of_range"),
        ),
        F.when(
            F.col("rpm").isNotNull()
            & (
                (F.col("rpm") < F.lit(quality.min_rpm))
                | (F.col("rpm") > F.lit(quality.max_rpm))
            ),
            F.lit("rpm_out_of_range"),
        ),
        F.when(F.col("engine_temp").isNull(), F.lit("engine_temp_missing")),
        F.when(
            F.col("engine_temp").isNotNull()
            & (
                (F.col("engine_temp") < F.lit(quality.min_engine_temp))
                | (F.col("engine_temp") > F.lit(quality.max_engine_temp))
            ),
            F.lit("engine_temp_out_of_range"),
        ),
        F.when(F.col("battery_level").isNull(), F.lit("battery_level_missing")),
        F.when(
            F.col("battery_level").isNotNull()
            & (
                (F.col("battery_level") < F.lit(quality.min_battery_level))
                | (F.col("battery_level") > F.lit(quality.max_battery_level))
            ),
            F.lit("battery_level_out_of_range"),
        ),
        F.when(F.col("latitude").isNull(), F.lit("latitude_missing")),
        F.when(
            F.col("latitude").isNotNull()
            & (
                (F.col("latitude") < F.lit(quality.min_latitude))
                | (F.col("latitude") > F.lit(quality.max_latitude))
            ),
            F.lit("latitude_out_of_range"),
        ),
        F.when(F.col("longitude").isNull(), F.lit("longitude_missing")),
        F.when(
            F.col("longitude").isNotNull()
            & (
                (F.col("longitude") < F.lit(quality.min_longitude))
                | (F.col("longitude") > F.lit(quality.max_longitude))
            ),
            F.lit("longitude_out_of_range"),
        ),
        F.when(~F.col("fault_code").isin(valid_fault_codes), F.lit("invalid_fault_code")),
    ]

    return (
        dataframe.withColumn("quality_errors", F.array(*error_columns))
        .withColumn(
            "quality_errors",
            F.expr("filter(quality_errors, item -> item is not null)"),
        )
        .withColumn("is_valid", F.size(F.col("quality_errors")) == F.lit(0))
    )

