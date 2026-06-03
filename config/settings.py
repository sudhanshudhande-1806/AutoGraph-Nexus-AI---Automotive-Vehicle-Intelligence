"""
Application configuration and settings.
"""
import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "src" / "ml" / "models"

# Backend Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# Frontend Configuration  
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "127.0.0.1")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))

# Database Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Kafka Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC_TELEMETRY = "vehicle-telemetry"
KAFKA_TOPIC_EVENTS = "vehicle-events"

# Airflow Configuration
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", str(PROJECT_ROOT / "data_pipeline" / "airflow"))

# Feature Flags
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
TESTING = os.getenv("TESTING", "False").lower() == "true"

# Data Configuration
CSV_FILE_VEHICLES = str(DATA_DIR / "silver_vehicle_data.csv")
CSV_FILE_TELEMETRY = str(DATA_DIR / "vehicle_telemetry.csv")
CSV_FILE_LOCATIONS = str(DATA_DIR / "vehicle_locations.csv")

# API Configuration
API_TITLE = "AutoGraph Nexus AI API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Fleet Management and Predictive Maintenance API"

# ML Model Configuration
MODEL_FAILURE_PREDICTION = str(MODELS_DIR / "failure_predictor.pkl")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
