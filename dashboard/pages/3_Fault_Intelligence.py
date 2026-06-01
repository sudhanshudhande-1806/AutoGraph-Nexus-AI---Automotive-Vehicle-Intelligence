import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠️ Fault Intelligence")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

faults = (
    df["fault_code"]
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
    y="count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)