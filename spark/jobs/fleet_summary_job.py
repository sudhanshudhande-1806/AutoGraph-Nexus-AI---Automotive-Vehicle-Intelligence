from pyspark.sql import functions as F

from spark.utils.spark_session import create_spark_session
from spark.utils.config_loader import load_module_config


config = load_module_config()

spark = create_spark_session(
    config=config,
    app_name="FleetSummary"
)

df = spark.read.parquet(
    config.storage.silver_path
)

summary = df.agg(
    F.countDistinct("vehicle_id").alias(
        "fleet_size"
    ),
    F.avg("speed").alias(
        "avg_speed"
    ),
    F.avg("engine_temp").alias(
        "avg_engine_temp"
    ),
    F.avg("battery_level").alias(
        "avg_battery"
    )
)

summary.show()