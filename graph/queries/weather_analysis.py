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

with driver.session() as session:

    result = session.run(
        """
        MATCH
        (v:Vehicle)-[:EXPERIENCED_WEATHER]->
        (w:Weather)

        RETURN
        w.weather,
        count(*) as total

        ORDER BY total DESC
        """
    )

    print("\nWEATHER DISTRIBUTION\n")

    for row in result:

        print(row["w.weather"], row["total"])