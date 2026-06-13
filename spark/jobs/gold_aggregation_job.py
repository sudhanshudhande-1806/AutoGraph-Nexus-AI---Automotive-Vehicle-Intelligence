from pyspark.sql import functions as F

from spark.utils.spark_session import create_spark_session
from spark.utils.config_loader import load_module_config


def main():

    config = load_module_config()

    spark = create_spark_session(
        config=config,
        app_name="AutoGraph-Gold"
    )

    silver_df = spark.read.parquet(
        config.storage.silver_path
    )

    gold_df = (
        silver_df
        .groupBy("vehicle_id")
        .agg(
            F.avg("speed").alias("avg_speed"),
            F.avg("engine_temp").alias("avg_engine_temp"),
            F.max("battery_level").alias("battery_level"),
            F.count("*").alias("event_count")
        )
    )

    gold_df.write.mode(
        "overwrite"
    ).parquet(
        "spark/gold/fleet_kpis"
    )

    print("Gold Layer Created")


if __name__ == "__main__":
    main()