"""Kafka to Bronze Structured Streaming job."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from pyspark.sql.streaming import StreamingQuery

from spark.utils.config_loader import Module10Config, load_module_config
from spark.utils.logging_utils import get_logger, setup_logging
from spark.utils.spark_session import create_spark_session
from spark.utils.transformations import (
    build_bronze_dataframe,
    read_kafka_stream,
    write_stream_to_parquet,
)

LOGGER = get_logger(__name__)


def run(config: Module10Config, once: bool = False) -> StreamingQuery:
    """Start the Bronze streaming query."""
    spark = create_spark_session(
        config=config,
        app_name=f"{config.app_name}-bronze",
        enable_kafka=True,
    )

    LOGGER.info(
        "Starting Bronze stream from Kafka topic %s at %s",
        config.kafka.telemetry_topic,
        config.kafka.bootstrap_servers,
    )
    raw_df = read_kafka_stream(spark=spark, kafka=config.kafka)
    bronze_df = build_bronze_dataframe(raw_df)

    return write_stream_to_parquet(
        dataframe=bronze_df,
        output_path=config.storage.bronze_path,
        checkpoint_path=config.storage.bronze_checkpoint,
        partition_columns=("event_date",),
        trigger_processing_time=config.streaming.trigger_processing_time,
        output_mode=config.streaming.output_mode,
        once=once,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Run Kafka to Bronze stream.")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to spark_config.yaml. Defaults to spark/configs/spark_config.yaml.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process available data and stop when the stream is caught up.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    args = parse_args(argv)
    setup_logging()
    config = load_module_config(args.config)

    query: StreamingQuery | None = None
    try:
        query = run(config=config, once=args.once)
        LOGGER.info("Bronze stream started with query id %s", query.id)
        query.awaitTermination()
        return 0
    except KeyboardInterrupt:
        LOGGER.info("Bronze stream interrupted by user.")
        return 130
    except Exception:
        LOGGER.exception("Bronze stream failed.")
        return 1
    finally:
        if query is not None and query.isActive:
            query.stop()


if __name__ == "__main__":
    raise SystemExit(main())

