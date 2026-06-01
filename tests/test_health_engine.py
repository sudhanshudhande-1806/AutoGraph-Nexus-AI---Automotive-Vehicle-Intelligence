import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from lakehouse.silver.vehicle_health import calculate_health_score

score = calculate_health_score(
    10,
    130,
    "P0420"
)

print("Health Score:", score)