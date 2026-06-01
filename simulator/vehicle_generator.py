import random
from datetime import datetime

VEHICLE_MODELS = [
    "Tesla Model Y",
    "BMW iX",
    "Mercedes EQS",
    "Audi e-tron",
    "Volkswagen ID.4",
    "Porsche Taycan"
]

def generate_vehicle():

    return {
        "vehicle_id": f"VH-{random.randint(1000,9999)}",

        "model": random.choice(VEHICLE_MODELS),

        "speed": random.randint(0,160),

        "rpm": random.randint(700,7000),

        "engine_temp": random.randint(70,130),

        "battery_level": random.randint(10,100),

        "timestamp": datetime.utcnow().isoformat()
    }