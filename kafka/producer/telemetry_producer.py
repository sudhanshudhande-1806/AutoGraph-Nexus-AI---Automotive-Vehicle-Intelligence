import os
import sys
import json
import time

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

from kafka import KafkaProducer