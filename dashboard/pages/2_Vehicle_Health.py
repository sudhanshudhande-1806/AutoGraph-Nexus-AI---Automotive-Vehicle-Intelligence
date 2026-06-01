import streamlit as st
import pandas as pd
import plotly.express as px

import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
DASHBOARD_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.insert(0, DASHBOARD_DIR)

from components.sidebar import render_sidebar

render_sidebar()

st.title("Vehicle Health")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

fig = px.histogram(
    df,
    x="health_score",
    nbins=10,
    title="Vehicle Health Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    df[
        [
            "vehicle_id",
            "health_score",
            "risk_level"
        ]
    ]
)
risk_counts = (
    df["risk_level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "risk",
    "count"
]

pie = px.pie(
    risk_counts,
    names="risk",
    values="count",
    title="Fleet Risk Distribution"
)

st.plotly_chart(
    pie,
    use_container_width=True
)