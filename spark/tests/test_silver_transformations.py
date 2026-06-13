"""Silver transformation tests."""

from __future__ import annotations

from datetime import datetime

from pyspark.sql import Row

from spark.utils.config_loader import DataQualitySettings
from spark.utils.schemas import BRONZE_SCHEMA
from spark.utils.transformations import build_silver_dataframe


def test_build_silver_dataframe_standardizes_and_deduplicates(spark_session) -> None:
    bronze_df = spark_session.createDataFrame(
        [
            _bronze_row(source_offset=1),
            _bronze_row(source_offset=2),
            _bronze_row(
                source_offset=3,
                vehicle_id="vh-2002",
                event_timestamp=datetime(2026, 6, 3, 12, 5, 0),
                speed=999.0,
            ),
        ],
        schema=BRONZE_SCHEMA,
    )

    silver_df = build_silver_dataframe(
        bronze_df=bronze_df,
        quality=_quality_settings(),
        watermark_delay=None,
    )
    rows = silver_df.collect()

    assert len(rows) == 1
    assert rows[0].vehicle_id == "VH-2001"
    assert rows[0].fault_code == "NONE"
    assert rows[0].severity == "NONE"
    assert rows[0].is_valid is True
    assert rows[0].quality_errors == []


def _bronze_row(
    source_offset: int,
    vehicle_id: str = " vh-2001 ",
    event_timestamp: datetime = datetime(2026, 6, 3, 12, 0, 0),
    speed: float = 64.0,
) -> Row:
    return Row(
        raw_payload="{}",
        source_topic="vehicle-telemetry",
        source_partition=0,
        source_offset=source_offset,
        kafka_timestamp=event_timestamp,
        vehicle_id=vehicle_id,
        model="Tesla Model Y",
        timestamp="2026-06-03T12:00:00",
        speed=speed,
        rpm=1800,
        engine_temp=86.0,
        battery_level=76.0,
        battery=None,
        fuel=None,
        latitude=18.52,
        longitude=73.86,
        fault_code=None,
        severity=None,
        weather="sunny",
        outside_temperature=30.0,
        last_service_days=12,
        service_type="battery check",
        ingest_timestamp=event_timestamp,
        event_timestamp=event_timestamp,
        event_date=event_timestamp.date(),
        parse_error=False,
        record_id=f"record-{source_offset}",
    )


def _quality_settings() -> DataQualitySettings:
    return DataQualitySettings(
        required_columns=(
            "vehicle_id",
            "event_timestamp",
            "speed",
            "engine_temp",
            "battery_level",
            "latitude",
            "longitude",
        ),
        valid_fault_codes=("NONE", "P0420", "P0300", "P0171", "P0455", "P0128"),
        min_speed=0,
        max_speed=250,
        min_rpm=0,
        max_rpm=9000,
        min_engine_temp=40,
        max_engine_temp=160,
        min_battery_level=0,
        max_battery_level=100,
        min_latitude=-90,
        max_latitude=90,
        min_longitude=-180,
        max_longitude=180,
    )
