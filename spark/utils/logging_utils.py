"""Logging helpers for Spark jobs."""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOGGING_PATH = PROJECT_ROOT / "spark" / "configs" / "logging.yaml"


def setup_logging(config_path: str | Path | None = None) -> None:
    """Configure Python logging from YAML, with a safe console fallback."""
    path = Path(config_path) if config_path else DEFAULT_LOGGING_PATH
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    if path.exists():
        with path.open("r", encoding="utf-8") as logging_file:
            logging_config = yaml.safe_load(logging_file) or {}
        logging.config.dictConfig(logging_config)
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger."""
    return logging.getLogger(f"autograph.spark.{name}")

