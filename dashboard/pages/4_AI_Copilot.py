import streamlit as st
import pandas as pd

st.title("🤖 AI Copilot")

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

question = st.text_input(
    "Ask a Question"
)

if question:

    if "critical" in question.lower():

        st.dataframe(
            df[
                df["risk_level"] == "HIGH"
            ]
        )

    elif "fault" in question.lower():

        st.write(
            df["fault_code"]
            .value_counts()
        )

    else:

        st.info(
            "Question not supported yet"
        )