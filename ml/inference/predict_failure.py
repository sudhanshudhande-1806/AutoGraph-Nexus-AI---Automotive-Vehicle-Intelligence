import joblib
import pandas as pd

model = joblib.load(
    "ml/models/failure_predictor.pkl"
)

sample = pd.DataFrame(
    [[20,130,25]],
    columns=[
        "battery_level",
        "engine_temp",
        "health_score"
    ]
)

prediction = model.predict(sample)

print(
    "Predicted Failure:",
    prediction[0]
)