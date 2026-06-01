import pandas as pd

def load_vehicle_data():

    df = pd.read_csv(
        "data/silver_vehicle_data.csv"
    )

    return df