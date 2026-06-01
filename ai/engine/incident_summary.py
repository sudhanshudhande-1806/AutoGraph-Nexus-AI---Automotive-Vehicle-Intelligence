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

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

critical = df[
    df["risk_level"] == "HIGH"
]

print("\nAI INCIDENT SUMMARY\n")

for _, row in critical.iterrows():

    print(
        f"""
Vehicle {row['vehicle_id']}
Health Score: {row['health_score']}
Risk Level: {row['risk_level']}

Recommended Action:
Immediate Maintenance
"""
    )