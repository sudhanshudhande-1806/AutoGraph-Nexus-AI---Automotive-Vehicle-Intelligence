# File Structure Improvement Guide

## Current Status

This guide explains the recommended file structure improvements for the AutoGraph-Nexus-AI project and provides instructions to implement them.

## Why Restructure?

The current flat structure makes it difficult to:
- Understand module organization
- Navigate large projects
- Scale for team collaboration
- Follow Python packaging standards

## Target Structure

```
AutoGraph-Nexus-AI/
├── src/                              # All source code
│   ├── __init__.py
│   ├── core/                         # Shared utilities
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management
│   │   ├── logger.py                 # Logging setup
│   │   └── database.py               # Database connections
│   ├── simulator/                    # Vehicle telemetry simulation
│   │   ├── __init__.py
│   │   ├── vehicle_generator.py
│   │   ├── telemetry_engine.py
│   │   ├── gps_generator.py
│   │   ├── fault_generator.py
│   │   ├── maintenance_generator.py
│   │   └── weather_generator.py
│   ├── kafka/                        # Event streaming
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   └── kafka_config.py
│   │   ├── producer/
│   │   │   └── telemetry_producer.py
│   │   └── consumer/
│   │       └── telemetry_consumer.py
│   ├── spark/                        # Spark processing
│   │   ├── __init__.py
│   │   ├── bronze/
│   │   │   ├── __init__.py
│   │   │   └── bronze_ingestion.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── vehicle_schema.py
│   ├── lakehouse/                    # Data architecture
│   │   ├── __init__.py
│   │   ├── silver/
│   │   │   ├── __init__.py
│   │   │   ├── silver_transform.py
│   │   │   ├── vehicle_health.py
│   │   │   ├── risk_engine.py
│   │   │   └── quality_rules.py
│   │   └── gold/
│   │       ├── __init__.py
│   │       ├── vehicle_rankings.py
│   │       ├── maintenance_queue.py
│   │       ├── fleet_health.py
│   │       ├── fault_trends.py
│   │       └── executive_kpis.py
│   ├── graph/                        # Neo4j knowledge graph
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   └── neo4j_config.py
│   │   ├── loaders/
│   │   │   └── graph_loader.py
│   │   ├── queries/
│   │   │   ├── vehicle_faults.py
│   │   │   ├── root_cause.py
│   │   │   ├── maintenance_graph.py
│   │   │   ├── weather_analysis.py
│   │   │   └── ai_root_cause.py
│   │   └── visualizations/
│   │       └── graph_dashboard.py
│   ├── ml/                           # Machine learning
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   └── failure_predictor.pkl
│   │   ├── training/
│   │   │   └── train_failure_model.py
│   │   └── inference/
│   │       └── predict_failure.py
│   ├── ai/                           # AI engine
│   │   ├── __init__.py
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── query_engine.py
│   │   │   └── incident_summary.py
│   │   └── knowledge_base/
│   │       ├── __init__.py
│   │       └── vehicle_data_loader.py
│   ├── dashboard/                    # Streamlit UI
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── theme.py
│   │   │   ├── sidebar.py
│   │   │   ├── page_banner.py
│   │   │   ├── metric_cards.py
│   │   │   ├── kpi_cards.py
│   │   │   └── futuristic_header.py
│   │   ├── pages/
│   │   │   ├── 0_Executive_Dashboard.py
│   │   │   ├── 1_Fleet_Overview.py
│   │   │   ├── 2_Vehicle_Health.py
│   │   │   ├── 3_Fault_Intelligence.py
│   │   │   ├── 4_AI_Copilot.py
│   │   │   ├── 5_Knowledge_Graph.py
│   │   │   ├── 6_Maintenance_Queue.py
│   │   │   ├── 7_Vehicle_Map.py
│   │   │   └── 8_Real_Time_Streaming.py
│   │   ├── assets/
│   │   │   ├── style.css
│   │   │   └── logo.png
│   │   └── services/
│   │       └── api.py
│   └── backend/                      # FastAPI backend
│       └── main.py
│
├── config/                           # Configuration files
│   ├── docker-compose.yml            # Service orchestration
│   ├── docker-compose.dev.yml        # Development setup
│   ├── .env.example                  # Environment template
│   └── settings.yaml                 # Application settings
│
├── infrastructure/                   # Deployment & setup
│   ├── docker/
│   ├── docker-compose-neo4j.yml
│   ├── airflow/
│   │   ├── airflow.cfg
│   │   ├── airflow.db
│   │   ├── webserver_config.py
│   │   ├── docker-compose.yml
│   │   └── dags/
│   │       └── vehicle_pipeline.py
│   └── .gitkeep
│
├── tests/                            # Test suite
│   ├── test_import.py                # Import tests
│   ├── test_spark.py                 # Spark tests
│   ├── test_health_engine.py         # Health engine tests
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   ├── fixtures/                     # Test fixtures
│   └── conftest.py                   # Pytest configuration
│
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index
│   ├── architecture.md               # System architecture
│   ├── setup.md                      # Installation guide
│   ├── api.md                        # API documentation
│   └── troubleshooting.md            # Troubleshooting guide
│
├── scripts/                          # Utility scripts
│   └── check_bronze.py               # Data quality checks
│
├── data/                             # Data directory (git-ignored)
│   ├── raw/                          # Raw data
│   ├── processed/                    # Processed data
│   └── models/                       # Trained models
│
├── logs/                             # Log files (git-ignored)
│
├── notebooks/                        # Jupyter notebooks
│
├── .gitignore                        # Git ignore rules
├── README.md                         # Main README
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package setup
├── pyproject.toml                    # Python project config
└── dbt/                              # dbt project (if used)

```

## How to Apply This Structure

### Option 1: Automated Script (Recommended)

Run the provided restructuring script:

```bash
python restructure_final.py
```

This script will:
1. Create all necessary directories
2. Move modules to `src/`
3. Move test files to `tests/`
4. Move docker-compose to `config/`
5. Create `__init__.py` files
6. Create documentation templates

### Option 2: Manual Steps

1. **Create directories:**
```bash
mkdir -p src/core config docs data logs notebooks
```

2. **Move modules:**
```bash
# Move each module
mv simulator src/
mv kafka src/
mv spark src/
mv lakehouse src/
mv graph src/
mv ml src/
mv ai src/
mv dashboard src/
mv backend src/
```

3. **Move test files:**
```bash
mv test_import.py tests/
mv test_spark.py tests/
```

4. **Move docker-compose:**
```bash
mv docker-compose.yml config/
```

5. **Create __init__.py:**
```bash
touch src/__init__.py
touch src/core/__init__.py
```

6. **Update imports:**
   - Change `from simulator` to `from src.simulator`
   - Change `from kafka` to `from src.kafka`
   - Update other relative imports accordingly

## Key Improvements

✅ **Clear Organization**: All source code under `src/` with logical submodules
✅ **Configuration**: Centralized in `config/` directory
✅ **Testing**: Tests organized in dedicated `tests/` directory
✅ **Documentation**: Comprehensive docs in `docs/`
✅ **Scalability**: Easy to add new modules and maintain team collaboration
✅ **Standards**: Follows Python packaging best practices

## What Changes for Developers

### Before (Old Structure)
```python
from simulator import vehicle_generator
from kafka.config import kafka_config
from dashboard.app import app
```

### After (New Structure)
```python
from src.simulator import vehicle_generator
from src.kafka.config import kafka_config
from src.dashboard.app import app
```

## Additional Files to Create

After restructuring, consider creating:

1. **`pyproject.toml`** - Python packaging configuration
2. **`requirements.txt`** - Python dependencies
3. **`setup.py`** - Package installer script
4. **`.env.example`** - Environment variables template

## Git Considerations

If using git, preserve history with:
```bash
# Instead of: rm -rf old_location
# Use: git mv old_location new_location
```

The automated script uses `git mv` to preserve commit history.

## Next Steps

1. Run the restructuring script
2. Update all import statements in your code
3. Update README.md with new structure
4. Run tests to verify everything works
5. Commit changes: `git commit -m "Restructure: improve file structure clarity"`

## Support

If you encounter issues:
1. Check `docs/troubleshooting.md`
2. Verify all imports have been updated
3. Ensure all directories exist
4. Check file permissions

