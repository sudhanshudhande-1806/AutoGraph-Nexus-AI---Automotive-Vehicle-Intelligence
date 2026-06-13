from spark.utils.spark_session import create_spark_session
from spark.utils.config_loader import load_module_config

config = load_module_config()

spark = create_spark_session(
    config=config,
    app_name="Check-Gold"
)

df = spark.read.parquet(
    "spark/gold/fleet_kpis"
)

df.show(
    truncate=False
)