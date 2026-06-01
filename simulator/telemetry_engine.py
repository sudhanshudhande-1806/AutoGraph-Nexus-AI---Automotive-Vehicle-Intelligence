import json
import time

from vehicle_generator import generate_vehicle
from gps_generator import generate_gps
from fault_generator import generate_fault
from weather_generator import generate_weather
from maintenance_generator import generate_maintenance

print(
    "AutoGraph Nexus AI Simulator Started"
)

while True:

    event = {

        **generate_vehicle(),

        **generate_gps(),

        **generate_fault(),

        **generate_weather(),

        **generate_maintenance()
    }

    print(
        json.dumps(
            event,
            indent=4
        )
    )

    time.sleep(2)