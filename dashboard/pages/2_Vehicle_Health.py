import streamlit as st
import pandas as pd
import plotly.express as px

import os
import sys

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

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

# --------------------------------------------------
# IMPORT COMPONENTS
# --------------------------------------------------

from components.sidebar import render_sidebar
from components.theme import load_theme

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

render_sidebar()
load_theme()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(
    "data/silver_vehicle_data.csv"
)

# --------------------------------------------------
# AI HEADER
# --------------------------------------------------

st.markdown(
"""
<div style="
background:linear-gradient(
135deg,
#0f172a,
#1e40af,
#7c3aed
);
padding:35px;
border-radius:25px;
box-shadow:0px 0px 40px rgba(59,130,246,0.5);
margin-bottom:30px;
">

<h1 style="
color:white;
font-size:55px;
margin-bottom:10px;
">
🔋 Vehicle Health Analytics
</h1>

<p style="
color:#dbeafe;
font-size:20px;
">
AI-Powered Fleet Monitoring & Predictive Maintenance
</p>

</div>
""",
unsafe_allow_html=True
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

avg_health = round(
    df["health_score"].mean(),
    2
)

critical = len(
    df[df["risk_level"] == "HIGH"]
)

healthy = len(
    df[df["risk_level"] == "LOW"]
)

attention = len(
    df[df["risk_level"] == "MEDIUM"]
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💚 Fleet Health",
        avg_health
    )

with c2:
    st.metric(
        "✅ Healthy",
        healthy
    )

with c3:
    st.metric(
        "⚠️ Attention",
        attention
    )

with c4:
    st.metric(
        "🚨 Critical",
        critical
    )

st.markdown("---")

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.histogram(
        df,
        x="health_score",
        nbins=10,
        title="Health Score Distribution"
    )

    fig.update_layout(
        paper_bgcolor="#081020",
        plot_bgcolor="#081020",
        font_color="white",
        title_font_size=22,
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    risk = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk.columns = [
        "risk",
        "count"
    ]

    pie = px.pie(
        risk,
        names="risk",
        values="count",
        hole=0.70,
        title="Fleet Risk Distribution"
    )

    pie.update_layout(
        paper_bgcolor="#081020",
        plot_bgcolor="#081020",
        font_color="white",
        title_font_size=22,
        height=450
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------------------------
# LEADERBOARD
# --------------------------------------------------

st.markdown(
"""
<h2 style="
color:white;
font-size:36px;
">
🏆 Fleet Health Leaderboard
</h2>
""",
unsafe_allow_html=True
)

ranking = df.sort_values(
    by="health_score",
    ascending=False
)

st.dataframe(
    ranking[
        [
            "vehicle_id",
            "health_score",
            "risk_level",
            "fault_code"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# CRITICAL VEHICLES
# --------------------------------------------------

st.markdown(
"""
<div style="
background:#3b0a0a;
padding:15px;
border-radius:15px;
border-left:6px solid red;
margin-top:25px;
margin-bottom:20px;
">

<h2 style="
color:#ff4d4d;
">
🚨 Critical Vehicles Requiring Immediate Action
</h2>

</div>
""",
unsafe_allow_html=True
)

critical_df = df[
    df["risk_level"] == "HIGH"
]

st.dataframe(
    critical_df,
    use_container_width=True
)

# --------------------------------------------------
# AI STATUS
# --------------------------------------------------

st.success(
"""
🟢 AI Fleet Copilot Online

• Telemetry Monitoring Active

• Knowledge Graph Connected

• Predictive Maintenance Enabled

• Neo4j Connected

• Fleet Risk Analysis Running
"""
)

# --------------------------------------------------
# LIVE EVENTS
# --------------------------------------------------

st.markdown(
"""
<h2 style="
color:white;
">
📡 Live Fleet Events
</h2>
""",
unsafe_allow_html=True
)

events = [
    "Vehicle VH-6707 reported P0455",
    "Vehicle VH-7812 battery health critical",
    "Maintenance queue updated",
    "Telemetry stream healthy",
    "Neo4j sync completed"
]

for e in events:

    st.markdown(
        f"""
        <div style="
        background:#101827;
        border-left:5px solid #3b82f6;
        padding:12px;
        margin-bottom:10px;
        border-radius:12px;
        color:white;
        ">
        ⚡ {e}
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# AI CONTROL CENTER
# --------------------------------------------------

st.markdown(
"""
<div style="
background:linear-gradient(
90deg,
#00c853,
#00b0ff
);
padding:25px;
border-radius:20px;
margin-top:30px;
">

<h2 style="
color:white;
">
🤖 AI Control Center
</h2>

<p style="
color:white;
font-size:16px;
">

● Fleet Telemetry Online<br>

● Knowledge Graph Active<br>

● Predictive Maintenance Running<br>

● AI Copilot Ready<br>

● Neo4j Synced

</p>

</div>
""",
unsafe_allow_html=True
)