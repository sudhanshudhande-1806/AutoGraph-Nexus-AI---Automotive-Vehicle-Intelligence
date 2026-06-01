from pyspark.sql.types import *

vehicle_schema = StructType([
    StructField("vehicle_id", StringType(), True),
    StructField("model", StringType(), True),
    StructField("speed", IntegerType(), True),
    StructField("rpm", IntegerType(), True),
    StructField("engine_temp", IntegerType(), True),
    StructField("battery_level", IntegerType(), True),
    StructField("timestamp", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("fault_code", StringType(), True),
    StructField("severity", StringType(), True),
    StructField("weather", StringType(), True),
    StructField("outside_temperature", IntegerType(), True),
    StructField("last_service_days", IntegerType(), True),
    StructField("service_type", StringType(), True)
])