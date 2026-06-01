import os
import sys

CURRENT_DIR = os.path.dirname(__file__)

DASHBOARD_DIR = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        ".."
    )
)

sys.path.insert(
    0,
    DASHBOARD_DIR
)

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar

render_sidebar()

st.title("⚡ Real-Time Fleet Telemetry")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

st.metric(
    "Vehicles",
    len(df)
)

st.metric(
    "Critical Vehicles",
    len(
        df[
            df["risk_level"]=="HIGH"
        ]
    )
)

st.dataframe(
    df,
    use_container_width=True
)