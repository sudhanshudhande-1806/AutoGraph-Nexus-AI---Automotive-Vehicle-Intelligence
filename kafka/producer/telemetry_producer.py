from kafka import KafkaProducer
import json
import time
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../simulator"
        )
    )
)

from vehicle_generator import generate_vehicle
from gps_generator import generate_gps
from fault_generator import generate_fault
from weather_generator import generate_weather
from maintenance_generator import generate_maintenance

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:
        json.dumps(v).encode("utf-8")
)

print("Producer Started...")

while True:

    event = {

        **generate_vehicle(),
        **generate_gps(),
        **generate_fault(),
        **generate_weather(),
        **generate_maintenance()

    }

    producer.send(
        "vehicle-telemetry",
        event
    )

    print(event)

    time.sleep(1)