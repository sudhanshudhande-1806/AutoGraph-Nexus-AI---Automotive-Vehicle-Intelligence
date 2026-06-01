import random

def generate_maintenance():

    return {

        "last_service_days":

        random.randint(
            1,
            365
        ),

        "service_type":

        random.choice(
            [
                "Oil Change",
                "Brake Service",
                "Battery Check",
                "Tyre Rotation"
            ]
        )
    }