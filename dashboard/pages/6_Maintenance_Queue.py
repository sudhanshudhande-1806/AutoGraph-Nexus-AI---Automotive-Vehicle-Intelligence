import streamlit as st
import pandas as pd

st.title("🔧 Maintenance Queue")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

critical = df[
    df["risk_level"] == "HIGH"
]

critical = critical.sort_values(
    by="health_score"
)

st.dataframe(critical)