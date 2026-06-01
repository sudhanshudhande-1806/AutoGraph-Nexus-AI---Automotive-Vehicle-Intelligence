import streamlit as st
import pandas as pd

import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
DASHBOARD_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.insert(0, DASHBOARD_DIR)

from components.sidebar import render_sidebar

render_sidebar()

st.title("Fleet Overview")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Fleet Size",
        len(df)
    )

with col2:
    st.metric(
        "Critical Vehicles",
        len(
            df[df["risk_level"] == "HIGH"]
        )
    )

with col3:
    st.metric(
        "Average Health",
        round(
            df["health_score"].mean(),
            2
        )
    )

st.dataframe(df)