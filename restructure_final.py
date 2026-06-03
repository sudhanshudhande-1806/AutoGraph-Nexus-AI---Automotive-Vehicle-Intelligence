#!/usr/bin/env python3
"""
Final restructuring script for AutoGraph-Nexus-AI
"""
import os
import shutil
from pathlib import Path

def safe_move(src, dst, use_copy=False):
    """Safely move a file or directory."""
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists():
        print(f"✗ Source does not exist: {src}")
        return False
    
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if use_copy:
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            shutil.rmtree(src_path) if src_path.is_dir() else os.remove(src_path)
        else:
            shutil.move(str(src_path), str(dst_path))
        print(f"✓ Moved: {src} → {dst}")
        return True
    except Exception as e:
        print(f"✗ Error moving {src}: {e}")
        return False

def main():
    os.chdir(r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity')
    print(f"Working directory: {os.getcwd()}\n")
    
    # Step 1: Create directories
    print("=" * 60)
    print("Step 1: Creating new directories")
    print("=" * 60)
    
    dirs_to_create = [
        'src', 'src/core', 'config', 'docs', 'data', 'logs', 'notebooks'
    ]
    
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_name}")
    
    # Step 2: Move directories to src/
    print("\n" + "=" * 60)
    print("Step 2: Moving modules to src/")
    print("=" * 60)
    
    dirs_to_move = [
        ('simulator', 'src/simulator'),
        ('kafka', 'src/kafka'),
        ('spark', 'src/spark'),
        ('lakehouse', 'src/lakehouse'),
        ('graph', 'src/graph'),
        ('ml', 'src/ml'),
        ('ai', 'src/ai'),
        ('dashboard', 'src/dashboard'),
        ('backend', 'src/backend'),
    ]
    
    for src, dst in dirs_to_move:
        if Path(src).exists():
            safe_move(src, dst)
        else:
            print(f"- Skipped (not found): {src}")
    
    # Step 3: Move test files
    print("\n" + "=" * 60)
    print("Step 3: Moving test files to tests/")
    print("=" * 60)
    
    test_files = ['test_import.py', 'test_spark.py']
    for test_file in test_files:
        if Path(test_file).exists():
            safe_move(test_file, f'tests/{test_file}')
        else:
            print(f"- Skipped (not found): {test_file}")
    
    # Step 4: Move docker-compose
    print("\n" + "=" * 60)
    print("Step 4: Moving docker-compose.yml to config/")
    print("=" * 60)
    
    if Path('docker-compose.yml').exists():
        safe_move('docker-compose.yml', 'config/docker-compose.yml')
    else:
        print("- Skipped (not found): docker-compose.yml")
    
    # Step 5: Create __init__.py files
    print("\n" + "=" * 60)
    print("Step 5: Creating __init__.py files")
    print("=" * 60)
    
    init_files = [
        'src/__init__.py',
        'src/core/__init__.py',
    ]
    
    for init_file in init_files:
        Path(init_file).parent.mkdir(parents=True, exist_ok=True)
        Path(init_file).touch()
        print(f"✓ Created: {init_file}")
    
    # Step 6: Update .gitignore
    print("\n" + "=" * 60)
    print("Step 6: Updating .gitignore")
    print("=" * 60)
    
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if '/logs/' not in content:
            content += '\n\n# Logs directory\n/logs/\n'
            gitignore_path.write_text(content)
            print("✓ Updated .gitignore with /logs/")
        else:
            print("- /logs/ already in .gitignore")
    
    # Step 7: Create config templates
    print("\n" + "=" * 60)
    print("Step 7: Creating configuration templates")
    print("=" * 60)
    
    env_example = Path('config/.env.example')
    env_example.parent.mkdir(parents=True, exist_ok=True)
    if not env_example.exists():
        env_example.write_text("""# Environment Configuration for AutoGraph Nexus AI

# Kafka Configuration
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=vehicle_telemetry

# Spark Configuration
SPARK_MASTER=local[*]
SPARK_CHECKPOINT_DIR=./checkpoints

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Dashboard Configuration
STREAMLIT_PORT=8501
API_PORT=8000

# Logging
LOG_LEVEL=INFO
""")
        print("✓ Created: config/.env.example")
    else:
        print("- config/.env.example already exists")
    
    settings_yaml = Path('config/settings.yaml')
    if not settings_yaml.exists():
        settings_yaml.write_text("""# Application Settings

server:
  host: localhost
  port: 8000
  debug: false

kafka:
  brokers:
    - localhost:9092
  topics:
    vehicle_telemetry: vehicle_telemetry
  group_id: autograph_group

spark:
  master: local[*]
  app_name: AutoGraph-Nexus-AI
  log_level: WARN

neo4j:
  uri: bolt://localhost:7687
  user: neo4j
  password: password

dashboard:
  port: 8501
  theme: dark
  layout: wide

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
""")
        print("✓ Created: config/settings.yaml")
    else:
        print("- config/settings.yaml already exists")
    
    # Create documentation files
    print("\n" + "=" * 60)
    print("Step 8: Creating documentation")
    print("=" * 60)
    
    docs_files = {
        'docs/README.md': """# Documentation

This directory contains all project documentation.

## Contents

- **architecture.md** - System architecture and design
- **setup.md** - Setup and installation guide  
- **api.md** - API documentation
- **troubleshooting.md** - Common issues and solutions
""",
        'docs/architecture.md': """# System Architecture

## Overview

AutoGraph Nexus AI is an enterprise-grade automotive data platform combining real-time telemetry, streaming analytics, knowledge graphs, and machine learning.

## Data Flow

```
Vehicle Simulator → Kafka → Spark Streaming → Lakehouse (Bronze/Silver/Gold) → Neo4j + AI → Dashboard
```

## Key Components

- **Simulator** (`src/simulator/`) - Vehicle telemetry generation
- **Streaming** (`src/kafka/`) - Event streaming
- **Processing** (`src/spark/`) - Spark data transformation  
- **Lakehouse** (`src/lakehouse/`) - Data layers
- **Analytics** (`src/ml/`, `src/ai/`) - ML and AI
- **Frontend** (`src/dashboard/`, `src/backend/`) - User interfaces
- **Graph** (`src/graph/`) - Neo4j integration

See full documentation in this directory.
""",
        'docs/setup.md': """# Setup and Installation

## Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Git

## Quick Start

1. Clone repository
2. Create virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure: `cp config/.env.example .env`
5. Start services: `docker-compose -f config/docker-compose.yml up -d`
6. Run application

See [architecture.md](architecture.md) for detailed setup.
""",
        'docs/api.md': """# API Documentation

## FastAPI Backend

REST API available at `http://localhost:8000`

### Key Endpoints
- `GET /vehicles` - List vehicles
- `GET /fleet/health` - Fleet health overview
- `GET /analytics/kpis` - Key metrics

See source code in `src/backend/` for complete API details.
""",
        'docs/troubleshooting.md': """# Troubleshooting

## Docker Issues
- Check: `docker ps`
- Logs: `docker-compose logs`

## Kafka Issues  
- Verify broker on port 9092
- Check kafka_config.py

## Spark Issues
- Check: `docker logs spark-master`
- Verify data in Bronze layer

## Neo4j Issues
- Default credentials: neo4j/password
- Port: 7687

For more help, check architecture.md or raise an issue on GitHub.
"""
    }
    
    for filepath, content in docs_files.items():
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        if not Path(filepath).exists():
            Path(filepath).write_text(content)
            print(f"✓ Created: {filepath}")
        else:
            print(f"- Already exists: {filepath}")
    
    print("\n" + "=" * 60)
    print("✓ RESTRUCTURING COMPLETE!")
    print("=" * 60)
    print("\nNew structure:")
    print("  src/              - All source code modules")
    print("  config/           - Configuration files")
    print("  tests/            - Test suite")
    print("  docs/             - Documentation")
    print("  infrastructure/   - Deployment configs")
    print("  data/             - Data files (git-ignored)")
    print("  logs/             - Log files (git-ignored)")
    print("  notebooks/        - Jupyter notebooks")

if __name__ == '__main__':
    main()
