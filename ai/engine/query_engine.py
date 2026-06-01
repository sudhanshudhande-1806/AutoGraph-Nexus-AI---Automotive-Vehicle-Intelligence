import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(0, PROJECT_ROOT)

print("Project Root:", PROJECT_ROOT)

from ai.knowledge_base.vehicle_data_loader import load_vehicle_data

df = load_vehicle_data()

question = input(
    "\nAsk Question: "
).lower()

if "critical" in question:

    print(
        df[
            df["risk_level"] == "HIGH"
        ]
    )

elif "health" in question:

    print(
        df.sort_values(
            by="health_score"
        )
    )

elif "fault" in question:

    print(
        df["fault_code"]
        .value_counts()
    )

else:

    print(
        "Question not supported yet"
    )