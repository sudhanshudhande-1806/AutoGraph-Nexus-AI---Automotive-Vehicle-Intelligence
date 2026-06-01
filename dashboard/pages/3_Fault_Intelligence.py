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

st.title("⚠️ Fault Intelligence")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

faults = (
    df["fault_code"]
    .fillna("NO_FAULT")
    .value_counts()
    .reset_index()
)

faults.columns = [
    "fault_code",
    "count"
]

fig = px.bar(
    faults,
    x="fault_code",
    y="count",
    title="Fault Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(faults)

st.metric(
    "Unique Fault Types",
    faults.shape[0]
)