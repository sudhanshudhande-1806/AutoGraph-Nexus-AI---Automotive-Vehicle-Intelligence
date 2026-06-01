import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

df["failure"] = (
    df["risk_level"] == "HIGH"
).astype(int)

X = df[
    [
        "battery_level",
        "engine_temp",
        "health_score"
    ]
]

y = df["failure"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "ml/models/failure_predictor.pkl"
)

print("Model Saved")