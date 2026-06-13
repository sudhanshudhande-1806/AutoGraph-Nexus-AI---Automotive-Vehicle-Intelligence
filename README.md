# AutoGraph Nexus AI

Autonomous Vehicle Digital Twin & Intelligence Platform

## Module 10 Status

Spark ETL Pipeline is implemented with:

- Kafka to Bronze Structured Streaming
- Bronze to Silver Structured Streaming
- JSON schema parsing
- Null handling and standardization
- Data quality rules
- Duplicate removal
- Parquet output partitioned by event_date
- YAML config management
- Logging setup
- Docker support
- Pytest unit tests

## Run Module 10

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run tests:

```powershell
python -m pytest spark/tests -q
```

Start Kafka:

```powershell
docker compose up -d zookeeper kafka kafka-init
```

Start telemetry producer:

```powershell
python -m kafka.producer.telemetry_producer
```

Run Bronze:

```powershell
python -m spark.jobs.bronze_streaming_job --config spark/configs/spark_config.yaml
```

Run Silver:

```powershell
python -m spark.jobs.silver_streaming_job --config spark/configs/spark_config.yaml
```

Run containerized streaming:

```powershell
docker compose --profile streaming up --build
```

## Features

- Kafka Streaming
- Spark Structured Streaming
- Delta Lake
- Airflow
- dbt
- Great Expectations
- MLflow
- Neo4j
- GraphRAG
- AI Copilot
- Predictive Maintenance
