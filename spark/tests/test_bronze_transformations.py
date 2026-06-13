"""Bronze transformation tests."""

from __future__ import annotations

from datetime import datetime

from pyspark.sql import Row

from spark.utils.transformations import build_bronze_dataframe


def test_build_bronze_dataframe_parses_valid_kafka_payload(spark_session) -> None:
    kafka_df = spark_session.createDataFrame(
        [
            Row(
                value=(
                    '{"vehicle_id":"vh-1001","model":"Tesla Model Y",'
                    '"timestamp":"2026-06-03T12:00:00",'
                    '"speed":72,"rpm":2100,"engine_temp":91,'
                    '"battery_level":88,"latitude":18.55,"longitude":73.85,'
                    '"fault_code":null,"severity":null,"weather":"Sunny",'
                    '"outside_temperature":31,"last_service_days":24,'
                    '"service_type":"Battery Check"}'
                ),
                topic="vehicle-telemetry",
                partition=0,
                offset=7,
                timestamp=datetime(2026, 6, 3, 12, 0, 1),
            )
        ]
    )

    bronze_df = build_bronze_dataframe(kafka_df)
    row = bronze_df.collect()[0]

    assert row.vehicle_id == "vh-1001"
    assert row.source_topic == "vehicle-telemetry"
    assert row.source_offset == 7
    assert row.parse_error is False
    assert row.record_id is not None
    assert row.event_date is not None


def test_build_bronze_dataframe_flags_invalid_json(spark_session) -> None:
    kafka_df = spark_session.createDataFrame(
        [
            Row(
                value='{"vehicle_id":',
                topic="vehicle-telemetry",
                partition=0,
                offset=8,
                timestamp=datetime(2026, 6, 3, 12, 0, 2),
            )
        ]
    )

    bronze_df = build_bronze_dataframe(kafka_df)
    row = bronze_df.collect()[0]

    assert row.parse_error is True
    assert row.vehicle_id is None

