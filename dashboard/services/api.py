import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


def get_vehicles():

    response = requests.get(
        f"{API_URL}/vehicles"
    )

    return pd.DataFrame(
        response.json()
    )


def get_summary():

    response = requests.get(
        f"{API_URL}/fleet/summary"
    )

    return response.json()