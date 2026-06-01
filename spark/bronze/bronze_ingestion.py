from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from spark.schemas.vehicle_schema import vehicle_schema

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("VehicleBronzeLayer") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Reading Kafka Stream...")

raw_df = spark.readStream \
    .format("kafka") \
    .option(
        "kafka.bootstrap.servers",
        "localhost:9092"
    ) \
    .option(
        "subscribe",
        "vehicle-telemetry"
    ) \
    .option(
        "startingOffsets",
        "earliest"
    ) \
    .load()

json_df = raw_df.selectExpr(
    "CAST(value AS STRING)"
)

parsed_df = json_df.select(
    from_json(
        col("value"),
        vehicle_schema
    ).alias("data")
).select("data.*")

query = parsed_df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option(
        "path",
        "spark/output/bronze"
    ) \
    .option(
        "checkpointLocation",
        "spark/checkpoints/bronze"
    ) \
    .start()

print("Bronze Layer Started")

query.awaitTermination()