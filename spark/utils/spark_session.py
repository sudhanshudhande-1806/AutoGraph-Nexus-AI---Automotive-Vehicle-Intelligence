from pyspark.sql import SparkSession

from spark.utils.config_loader import Module10Config


def create_spark_session(
    config: Module10Config,
    app_name: str | None = None,
    enable_kafka: bool = False,
) -> SparkSession:

    builder = SparkSession.builder.appName(
        app_name or config.app_name
    )

    if config.spark.master:
        builder = builder.master(config.spark.master)

    builder = (
        builder
        .config(
            "spark.sql.session.timeZone",
            config.spark.timezone
        )
        .config(
            "spark.sql.shuffle.partitions",
            str(config.spark.shuffle_partitions)
        )
        .config(
            "spark.sql.parquet.compression.codec",
            config.storage.compression
        )
        .config(
            "spark.driver.host",
            "127.0.0.1"
        )
        .config(
            "spark.driver.bindAddress",
            "127.0.0.1"
        )
        .config(
            "spark.hadoop.io.native.lib.available",
            "false"
        )
        .config(
            "spark.hadoop.fs.file.impl",
            "org.apache.hadoop.fs.LocalFileSystem"
        )
        .config(
            "spark.sql.streaming.checkpointFileManagerClass",
            "org.apache.spark.sql.execution.streaming.CheckpointFileManager$FileSystemBasedCheckpointFileManager"
        )
    )

    for key, value in config.spark.extra_conf.items():
        builder = builder.config(
            key,
            value
        )

    if enable_kafka and config.spark.kafka_package:
        builder = builder.config(
            "spark.jars.packages",
            config.spark.kafka_package
        )

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel(
        config.spark.log_level
    )

    return spark