"""Bronze to Silver Structured Streaming job."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from pyspark.sql.streaming import StreamingQuery

from spark.utils.config_loader import Module10Config, load_module_config
from spark.utils.logging_utils import get_logger, setup_logging
from spark.utils.schemas import BRONZE_SCHEMA
from spark.utils.spark_session import create_spark_session
from spark.utils.transformations import (
    build_silver_dataframe,
    read_parquet_stream,
    write_stream_to_parquet,
)

LOGGER = get_logger(__name__)


def run(config: Module10Config, once: bool = False) -> StreamingQuery:
    """Start the Silver streaming query."""
    spark = create_spark_session(
        config=config,
        app_name=f"{config.app_name}-silver",
        enable_kafka=False,
    )

    LOGGER.info("Starting Silver stream from %s", config.storage.bronze_path)
    bronze_df = read_parquet_stream(
        spark=spark,
        path=config.storage.bronze_path,
        schema=BRONZE_SCHEMA,
    )
    silver_df = build_silver_dataframe(
        bronze_df=bronze_df,
        quality=config.data_quality,
        watermark_delay=config.streaming.watermark_delay,
    )

    return write_stream_to_parquet(
        dataframe=silver_df,
        output_path=config.storage.silver_path,
        checkpoint_path=config.storage.silver_checkpoint,
        partition_columns=("event_date",),
        trigger_processing_time=config.streaming.trigger_processing_time,
        output_mode=config.streaming.output_mode,
        once=once,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Run Bronze to Silver stream.")
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
        LOGGER.info("Silver stream started with query id %s", query.id)
        query.awaitTermination()
        return 0
    except KeyboardInterrupt:
        LOGGER.info("Silver stream interrupted by user.")
        return 130
    except Exception:
        LOGGER.exception("Silver stream failed.")
        return 1
    finally:
        if query is not None and query.isActive:
            query.stop()


if __name__ == "__main__":
    raise SystemExit(main())
