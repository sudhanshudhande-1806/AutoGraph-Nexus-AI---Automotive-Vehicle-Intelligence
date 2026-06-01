import pandas as pd

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

print("\nEXECUTIVE DASHBOARD\n")

print(
    "Fleet Size:",
    len(df)
)

print(
    "Average Health Score:",
    round(
        df["health_score"].mean(),
        2
    )
)

print(
    "Critical Vehicles:",
    len(
        df[
            df["risk_level"] == "HIGH"
        ]
    )
)

print(
    "Fault Events:",
    df["fault_code"].count()
)