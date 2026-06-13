"""Schema tests for vehicle telemetry."""

from __future__ import annotations

from spark.utils.schemas import TELEMETRY_SCHEMA


def test_telemetry_schema_contains_simulator_fields() -> None:
    field_names = {field.name for field in TELEMETRY_SCHEMA.fields}

    assert {
        "vehicle_id",
        "timestamp",
        "speed",
        "rpm",
        "engine_temp",
        "battery_level",
        "latitude",
        "longitude",
        "fault_code",
        "severity",
        "weather",
        "outside_temperature",
        "last_service_days",
        "service_type",
    }.issubset(field_names)


def test_telemetry_schema_supports_legacy_battery_and_fuel_fields() -> None:
    field_names = {field.name for field in TELEMETRY_SCHEMA.fields}

    assert "battery" in field_names
    assert "fuel" in field_names

