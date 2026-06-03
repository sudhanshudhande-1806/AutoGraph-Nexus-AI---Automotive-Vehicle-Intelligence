import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

from components.sidebar import render_sidebar
from components.theme import load_theme
import components.futuristic_header as fh

from components.kpi_cards import kpi_card
# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="AutoGraph Nexus AI",
    page_icon="🚗",
    layout="wide"
)

render_sidebar()

load_theme()

fh.render_header(
    "🚗 AutoGraph Nexus AI",
    "Connected Vehicle Intelligence Platform"
)
# --------------------------------------------------
# DATA
# --------------------------------------------------

import requests

API_URL = "http://127.0.0.1:8000"

response = requests.get(
    f"{API_URL}/vehicles"
)

df = pd.DataFrame(
    response.json()
)

from services.api import (
    get_vehicles,
    get_summary
)

# --------------------------------------------------
# KPI DATA
# --------------------------------------------------

fleet_size = summary[
    "fleet_size"
]

critical_count = summary[
    "critical_vehicles"
]

fault_count = summary[
    "fault_events"
]

avg_health = summary[
    "average_health"
]
# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Fleet Size",
        fleet_size
    )

with c2:
    kpi_card(
        "Critical Vehicles",
        critical_count
    )

with c3:
    kpi_card(
        "Fault Events",
        fault_count
    )

with c4:
    kpi_card(
        "Average Health",
        avg_health
    )

st.markdown("---")

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left, right = st.columns([2, 1])

with left:

    risk = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk.columns = [
        "risk",
        "count"
    ]

    fig = px.pie(
        risk,
        names="risk",
        values="count",
        hole=0.6,
        title="Fleet Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",

            value=df[
                "health_score"
            ].mean(),

            title={
                "text":
                "Fleet Health"
            },

            gauge={
                "axis":{
                    "range":[0,100]
                },

                "bar":{
                    "color":"lime"
                }
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------------------------
# ALERTS
# --------------------------------------------------

critical = df[
    df["risk_level"] == "HIGH"
]

st.error(
    f"""
    🚨 {critical_count}
    Critical Vehicles Need Immediate Attention
    """
)

# --------------------------------------------------
# CRITICAL VEHICLES
# --------------------------------------------------

st.subheader(
    "🚨 Critical Vehicles"
)

st.dataframe(
    critical[
        [
            "vehicle_id",
            "health_score",
            "fault_code",
            "service_type"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

# --------------------------------------------------
# FULL DATA
# --------------------------------------------------

st.subheader(
    "📊 Fleet Overview"
)

st.dataframe(
    df,
    use_container_width=True
)