import random

FAULT_CODES = [

    "P0420",
    "P0300",
    "P0171",
    "P0455",
    "P0128",

    None,
    None,
    None,
    None
]

def generate_fault():

    fault = random.choice(
        FAULT_CODES
    )

    return {

        "fault_code": fault,

        "severity":

        random.choice(
            [
                "LOW",
                "MEDIUM",
                "HIGH"
            ]
        )
        if fault
        else None
    }