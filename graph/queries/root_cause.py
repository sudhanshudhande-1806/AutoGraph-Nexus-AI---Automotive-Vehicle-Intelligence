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
        (v:Vehicle)-[:HAS_FAULT]->
        (f:Fault)

        RETURN
        f.fault_code AS fault,
        count(*) AS total

        ORDER BY total DESC
        """
    )

    print("\nROOT CAUSE ANALYSIS\n")

    for row in result:

        print(
            row["fault"],
            row["total"]
        )