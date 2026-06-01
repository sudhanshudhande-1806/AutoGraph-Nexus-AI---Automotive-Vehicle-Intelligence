import streamlit as st

st.set_page_config(
    page_title="AutoGraph Nexus AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>

    .main {
        background-color:#050816;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.title("🚗 AutoGraph Nexus AI")

st.subheader(
    "Connected Vehicle Intelligence Platform"
)

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Vehicles",
        "10"
    )

with c2:
    st.metric(
        "Critical",
        "3"
    )

with c3:
    st.metric(
        "Fault Events",
        "6"
    )

with c4:
    st.metric(
        "Avg Health",
        "61"
    )

st.markdown("---")

st.info(
    """
    Fleet Intelligence Platform

    • Real-Time Telemetry

    • Fault Analytics

    • AI Copilot

    • Knowledge Graph

    • Predictive Maintenance
    """
)