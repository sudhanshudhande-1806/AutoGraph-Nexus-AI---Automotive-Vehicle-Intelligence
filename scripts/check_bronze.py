from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("CheckBronze") \
    .getOrCreate()

df = spark.read.parquet(
    "spark/output/bronze"
)

print("Total Records:", df.count())

df.printSchema()

df.show(10, truncate=False)