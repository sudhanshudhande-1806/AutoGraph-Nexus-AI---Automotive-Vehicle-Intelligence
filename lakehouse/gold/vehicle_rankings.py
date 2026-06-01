import pandas as pd

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

ranked = df.sort_values(
    by="health_score",
    ascending=False
)

print("\nTOP VEHICLES\n")

print(
    ranked[
        [
            "vehicle_id",
            "health_score",
            "risk_level"
        ]
    ]
)