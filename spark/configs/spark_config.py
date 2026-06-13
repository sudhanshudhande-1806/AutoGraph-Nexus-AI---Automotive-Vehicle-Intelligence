from pyspark.sql import SparkSession


def create_spark_session():

    spark = (
        SparkSession.builder
        .appName("AutoGraphNexusAI")
        .master("local[*]")
        .config(
            "spark.sql.shuffle.partitions",
            "4"
        )
        .getOrCreate()
    )

    return spark