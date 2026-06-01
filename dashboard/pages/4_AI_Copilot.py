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

st.title("🤖 AI Fleet Copilot")

st.caption(
    "Ask questions about vehicle health, faults, maintenance, and fleet status."
)

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

question = st.text_input(
    "Ask Fleet AI",
    placeholder="Example: show critical vehicles"
)

if question:

    question = question.lower()

    if "critical" in question:

        st.subheader("🚨 Critical Vehicles")

        result = df[
            df["risk_level"] == "HIGH"
        ]

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            f"{len(result)} critical vehicles found."
        )

    elif "fault" in question:

        st.subheader("⚠️ Fault Analysis")

        faults = (
            df["fault_code"]
            .fillna("NO_FAULT")
            .value_counts()
        )

        st.dataframe(
            faults,
            use_container_width=True
        )

    elif "health" in question:

        st.subheader("💚 Vehicle Health Ranking")

        result = df.sort_values(
            by="health_score"
        )

        st.dataframe(
            result[
                [
                    "vehicle_id",
                    "health_score",
                    "risk_level"
                ]
            ],
            use_container_width=True
        )

    elif "healthy" in question:

        st.subheader("✅ Healthy Vehicles")

        result = df[
            df["risk_level"] == "LOW"
        ]

        st.dataframe(
            result,
            use_container_width=True
        )

    elif "maintenance" in question:

        st.subheader("🔧 Maintenance Queue")

        result = df[
            df["risk_level"] == "HIGH"
        ].sort_values(
            by="health_score"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

    else:

        st.warning(
            """
            Supported Questions:

            • show critical vehicles

            • show health scores

            • show fault codes

            • show healthy vehicles

            • show maintenance queue
            """
        )