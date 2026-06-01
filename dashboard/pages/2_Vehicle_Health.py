import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💚 Vehicle Health")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

fig = px.histogram(
    df,
    x="health_score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)