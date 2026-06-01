import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from neo4j import GraphDatabase
from graph.config.neo4j_config import *

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

with driver.session() as session:

    for _, row in df.iterrows():

        session.run(
            """
            MERGE (v:Vehicle {
                vehicle_id:$vehicle_id
            })

            MERGE (f:Fault {
                fault_code:$fault_code
            })

            MERGE (w:Weather {
                weather:$weather
            })

            MERGE (m:Maintenance {
                service_type:$service_type
            })

            MERGE (v)-[:HAS_FAULT]->(f)

            MERGE (v)-[:EXPERIENCED_WEATHER]->(w)

            MERGE (v)-[:RECEIVED_SERVICE]->(m)
            """,

            vehicle_id=row["vehicle_id"],
            fault_code=str(row["fault_code"]),
            weather=row["weather"],
            service_type=row["service_type"]
        )

print("Advanced Graph Loaded")