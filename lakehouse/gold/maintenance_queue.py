import pandas as pd

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

critical = df[
    df["risk_level"] == "HIGH"
]

critical = critical.sort_values(
    by="health_score"
)

print(
    "\nMAINTENANCE PRIORITY QUEUE\n"
)

print(
    critical[
        [
            "vehicle_id",
            "health_score",
            "risk_level"
        ]
    ]
)