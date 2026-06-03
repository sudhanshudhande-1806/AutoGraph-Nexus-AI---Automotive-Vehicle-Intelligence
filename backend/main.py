from fastapi import FastAPI
import pandas as pd
import numpy as np
import os
import json

app = FastAPI(
    title="AutoGraph Nexus AI API"
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "silver_vehicle_data.csv"
)


@app.get("/")
def home():
    return {
        "message": "AutoGraph Nexus AI Backend Running"
    }


@app.get("/vehicles")
def get_vehicles():

    try:

        df = pd.read_csv(CSV_FILE)

        # Replace Infinity values
        df.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True
        )

        # Replace NaN with None
        df = df.astype(object)
        df = df.where(
            pd.notnull(df),
            None
        )

        data = df.to_dict(
            orient="records"
        )

        # Force JSON-safe conversion
        json.dumps(data)

        return data

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/fleet/summary")
def fleet_summary():

    try:

        df = pd.read_csv(CSV_FILE)

        return {
            "fleet_size": int(len(df)),
            "critical_vehicles": int(
                len(
                    df[
                        df["risk_level"] == "HIGH"
                    ]
                )
            ),
            "average_health": float(
                round(
                    df["health_score"].mean(),
                    2
                )
            ),
            "fault_events": int(
                df["fault_code"]
                .notna()
                .sum()
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AutoGraph Nexus AI Backend"
    }