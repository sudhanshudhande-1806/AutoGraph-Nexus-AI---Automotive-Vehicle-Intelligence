import random

WEATHER = [

    "Sunny",
    "Cloudy",
    "Rain",
    "Fog",
    "Storm"
]

def generate_weather():

    return {

        "weather":
            random.choice(
                WEATHER
            ),

        "outside_temperature":
            random.randint(
                10,
                45
            )
    }