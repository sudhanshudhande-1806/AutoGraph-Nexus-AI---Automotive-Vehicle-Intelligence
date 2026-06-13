# Module 10: Spark ETL Pipeline

## Directory Structure

```text
spark/
  configs/
    logging.yaml
    spark_config.yaml
  jobs/
    bronze_streaming_job.py
    silver_streaming_job.py
  tests/
    conftest.py
    test_bronze_transformations.py
    test_schema.py
    test_silver_transformations.py
  utils/
    config_loader.py
    logging_utils.py
    quality_rules.py
    schemas.py
    spark_session.py
    transformations.py
  Dockerfile
  README.md
```

## Flow

```text
Kafka topic vehicle-telemetry
  -> Bronze Parquet: data/lakehouse/bronze/vehicle_telemetry
  -> Silver Parquet: data/lakehouse/silver/vehicle_telemetry
```

Bronze stores parsed telemetry plus source metadata, raw payloads, parse flags,
record ids, ingest timestamps, event timestamps, and event-date partitions.

Silver standardizes types and casing, handles nullable optional fields, applies
data quality rules, removes duplicates, and writes clean records partitioned by
event_date.

## Local Commands

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start Kafka:

```powershell
docker compose up -d zookeeper kafka kafka-init
```

Start the simulator producer:

```powershell
python -m kafka.producer.telemetry_producer
```

Run Bronze streaming:

```powershell
python -m spark.jobs.bronze_streaming_job --config spark/configs/spark_config.yaml
```

Run Silver streaming in a second terminal:

```powershell
python -m spark.jobs.silver_streaming_job --config spark/configs/spark_config.yaml
```

Run unit tests:

```powershell
python -m pytest spark/tests -q
```

## Docker Commands

Build and run the streaming services:

```powershell
docker compose --profile streaming up --build
```

## Expected Output

Bronze job logs:

```text
Starting Bronze stream from Kafka topic vehicle-telemetry at localhost:9092
Bronze stream started with query id ...
```

Silver job logs:

```text
Starting Silver stream from .../data/lakehouse/bronze/vehicle_telemetry
Silver stream started with query id ...
```

Parquet output:

```text
data/lakehouse/bronze/vehicle_telemetry/event_date=YYYY-MM-DD/*.parquet
data/lakehouse/silver/vehicle_telemetry/event_date=YYYY-MM-DD/*.parquet
```

Test output:

```text
5 passed
```

