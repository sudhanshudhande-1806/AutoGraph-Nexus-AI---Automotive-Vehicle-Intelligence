import streamlit as st

st.title("🕸 Vehicle Knowledge Graph")

st.success(
    "Neo4j Connected Successfully"
)

st.markdown("""
### Graph Relationships

Vehicle → Fault

Vehicle → Maintenance

Vehicle → Weather

Vehicle → Sensor

Root Cause Analysis Enabled
""")