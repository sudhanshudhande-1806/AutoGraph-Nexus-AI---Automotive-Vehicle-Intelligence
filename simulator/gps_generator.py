import random

def generate_gps():

    return {

        "latitude":
            round(
                random.uniform(
                    18.45,
                    18.65
                ),
                6
            ),

        "longitude":
            round(
                random.uniform(
                    73.75,
                    73.95
                ),
                6
            )
    }