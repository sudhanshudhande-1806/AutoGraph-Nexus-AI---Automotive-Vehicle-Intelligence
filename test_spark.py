from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("AutoGraphTest")
    .getOrCreate()
)

print("Spark Started Successfully")

spark.range(10).show()

spark.stop()