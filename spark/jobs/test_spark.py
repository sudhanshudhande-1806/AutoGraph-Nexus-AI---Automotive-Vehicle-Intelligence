from spark.configs.spark_config import (
    create_spark_session
)

spark = create_spark_session()

data = [
    ("VH-1001", 90),
    ("VH-1002", 75),
    ("VH-1003", 45)
]

df = spark.createDataFrame(
    data,
    ["vehicle_id", "health_score"]
)

df.show()