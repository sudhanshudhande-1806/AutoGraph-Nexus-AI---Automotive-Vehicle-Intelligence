import pandas as pd

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

faults = df["fault_code"].value_counts()

print("\nTOP FAULT CODES\n")

print(faults)