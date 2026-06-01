import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from lakehouse.silver.vehicle_health import calculate_health_score
from lakehouse.silver.risk_engine import classify_risk
from lakehouse.silver.risk_engine import vehicle_status

print("Loading dataset...")

df = pd.read_csv(
    "data/vehicle_telemetry.csv"
)

print("Records Loaded:", len(df))

health_scores = []
risk_levels = []
statuses = []

for _, row in df.iterrows():

    score = calculate_health_score(
        row["battery_level"],
        row["engine_temp"],
        row["fault_code"]
    )

    health_scores.append(score)

    risk_levels.append(
        classify_risk(score)
    )

    statuses.append(
        vehicle_status(score)
    )

df["health_score"] = health_scores
df["risk_level"] = risk_levels
df["vehicle_status"] = statuses

df.to_csv(
    "data/silver_vehicle_data.csv",
    index=False
)

print("Silver Layer Created Successfully")
print("Output File: data/silver_vehicle_data.csv")