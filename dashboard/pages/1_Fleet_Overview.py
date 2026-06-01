import streamlit as st
import pandas as pd

st.title("🚗 Fleet Overview")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

st.metric(
    "Fleet Size",
    len(df)
)

st.dataframe(df)