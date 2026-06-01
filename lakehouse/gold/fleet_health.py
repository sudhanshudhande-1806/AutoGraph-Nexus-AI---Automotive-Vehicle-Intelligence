import pandas as pd

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

total = len(df)

healthy = len(
    df[df["vehicle_status"] == "HEALTHY"]
)

attention = len(
    df[df["vehicle_status"] == "ATTENTION_REQUIRED"]
)

critical = len(
    df[df["vehicle_status"] == "CRITICAL"]
)

print("\nFLEET HEALTH REPORT\n")

print("Total Vehicles:", total)

print(
    "Healthy:",
    round(healthy / total * 100, 2),
    "%"
)

print(
    "Attention:",
    round(attention / total * 100, 2),
    "%"
)

print(
    "Critical:",
    round(critical / total * 100, 2),
    "%"
)