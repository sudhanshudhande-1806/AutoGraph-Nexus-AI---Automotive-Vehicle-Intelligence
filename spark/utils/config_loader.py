"""Configuration loading for Module 10 Spark jobs."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "spark" / "configs" / "spark_config.yaml"

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::([^}]*))?\}")


@dataclass(frozen=True)
class KafkaSettings:
    """Kafka source settings."""

    bootstrap_servers: str
    telemetry_topic: str
    starting_offsets: str
    fail_on_data_loss: bool


@dataclass(frozen=True)
class StorageSettings:
    """Storage paths used by Bronze and Silver streams."""

    bronze_path: str
    silver_path: str
    bronze_checkpoint: str
    silver_checkpoint: str
    compression: str


@dataclass(frozen=True)
class SparkSettings:
    """Spark runtime settings."""

    master: str | None
    log_level: str
    shuffle_partitions: int
    timezone: str
    kafka_package: str | None
    extra_conf: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class StreamingSettings:
    """Structured Streaming trigger settings."""

    trigger_processing_time: str
    watermark_delay: str
    output_mode: str


@dataclass(frozen=True)
class DataQualitySettings:
    """Data quality thresholds for vehicle telemetry."""

    required_columns: tuple[str, ...]
    valid_fault_codes: tuple[str, ...]
    min_speed: float
    max_speed: float
    min_rpm: float
    max_rpm: float
    min_engine_temp: float
    max_engine_temp: float
    min_battery_level: float
    max_battery_level: float
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float


@dataclass(frozen=True)
class Module10Config:
    """Complete configuration object for Module 10."""

    app_name: str
    environment: str
    spark: SparkSettings
    kafka: KafkaSettings
    storage: StorageSettings
    streaming: StreamingSettings
    data_quality: DataQualitySettings


def load_module_config(config_path: str | Path | None = None) -> Module10Config:
    """Load Module 10 configuration from YAML with environment overrides."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    if not path.exists():
        raise FileNotFoundError(f"Spark configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        raw_config = yaml.safe_load(config_file) or {}

    resolved = _resolve_env(raw_config)
    return _to_module_config(resolved)


def _resolve_env(value: Any) -> Any:
    """Resolve ${ENV_VAR:default} references inside loaded YAML values."""
    if isinstance(value, dict):
        return {key: _resolve_env(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_env(item) for item in value]
    if not isinstance(value, str):
        return value

    def replace(match: re.Match[str]) -> str:
        env_name = match.group(1)
        default = match.group(2) or ""
        return os.getenv(env_name, default)

    return _ENV_PATTERN.sub(replace, value)


def _to_module_config(raw: dict[str, Any]) -> Module10Config:
    app = raw.get("app", {})
    spark = raw.get("spark", {})
    kafka = raw.get("kafka", {})
    storage = raw.get("storage", {})
    streaming = raw.get("streaming", {})
    data_quality = raw.get("data_quality", {})

    return Module10Config(
        app_name=str(app.get("name", "AutoGraphNexusModule10")),
        environment=str(app.get("environment", "local")),
        spark=SparkSettings(
            master=_empty_to_none(spark.get("master")),
            log_level=str(spark.get("log_level", "WARN")),
            shuffle_partitions=int(spark.get("shuffle_partitions", 4)),
            timezone=str(spark.get("timezone", "UTC")),
            kafka_package=_empty_to_none(spark.get("kafka_package")),
            extra_conf={
                str(key): str(value)
                for key, value in (spark.get("extra_conf") or {}).items()
            },
        ),
        kafka=KafkaSettings(
            bootstrap_servers=str(kafka.get("bootstrap_servers", "localhost:9092")),
            telemetry_topic=str(kafka.get("telemetry_topic", "vehicle-telemetry")),
            starting_offsets=str(kafka.get("starting_offsets", "latest")),
            fail_on_data_loss=_as_bool(kafka.get("fail_on_data_loss", False)),
        ),
        storage=StorageSettings(
            bronze_path=_resolve_project_path(storage.get("bronze_path")),
            silver_path=_resolve_project_path(storage.get("silver_path")),
            bronze_checkpoint=_resolve_project_path(storage.get("bronze_checkpoint")),
            silver_checkpoint=_resolve_project_path(storage.get("silver_checkpoint")),
            compression=str(storage.get("compression", "snappy")),
        ),
        streaming=StreamingSettings(
            trigger_processing_time=str(
                streaming.get("trigger_processing_time", "10 seconds")
            ),
            watermark_delay=str(streaming.get("watermark_delay", "10 minutes")),
            output_mode=str(streaming.get("output_mode", "append")),
        ),
        data_quality=DataQualitySettings(
            required_columns=tuple(data_quality.get("required_columns", ())),
            valid_fault_codes=tuple(data_quality.get("valid_fault_codes", ())),
            min_speed=float(data_quality.get("min_speed", 0)),
            max_speed=float(data_quality.get("max_speed", 250)),
            min_rpm=float(data_quality.get("min_rpm", 0)),
            max_rpm=float(data_quality.get("max_rpm", 9000)),
            min_engine_temp=float(data_quality.get("min_engine_temp", 40)),
            max_engine_temp=float(data_quality.get("max_engine_temp", 160)),
            min_battery_level=float(data_quality.get("min_battery_level", 0)),
            max_battery_level=float(data_quality.get("max_battery_level", 100)),
            min_latitude=float(data_quality.get("min_latitude", -90)),
            max_latitude=float(data_quality.get("max_latitude", 90)),
            min_longitude=float(data_quality.get("min_longitude", -180)),
            max_longitude=float(data_quality.get("max_longitude", 180)),
        ),
    )


def _resolve_project_path(value: Any) -> str:
    if value is None:
        raise ValueError("Storage path configuration cannot be empty.")

    path = Path(str(value))
    if path.is_absolute():
        return str(path)
    return str(PROJECT_ROOT / path)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _empty_to_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None

