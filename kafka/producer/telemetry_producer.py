from kafka import KafkaProducer
import json
import time
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from simulator.vehicle_generator import generate_vehicle
from simulator.gps_generator import generate_gps
from simulator.fault_generator import generate_fault
from simulator.weather_generator import generate_weather
from simulator.maintenance_generator import generate_maintenance

print("Producer Started...")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

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