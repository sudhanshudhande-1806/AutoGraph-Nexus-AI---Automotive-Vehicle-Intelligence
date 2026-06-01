import os
import sys

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

fault = input("\nEnter Fault Code: ").upper()

with driver.session() as session:

    result = session.run(
        """
        MATCH (v:Vehicle)-[:HAS_FAULT]->(f:Fault)
        WHERE f.fault_code = $fault
        RETURN v.vehicle_id AS vehicle
        """,
        fault=fault
    )

    print("\nROOT CAUSE EXPLORER\n")

    found = False

    for row in result:
        found = True
        print(row["vehicle"])

    if not found:
        print("No vehicles found")