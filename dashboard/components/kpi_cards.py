import streamlit as st

def render_kpis(
    fleet,
    critical,
    faults,
    health
):

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Fleet",
        fleet
    )

    c2.metric(
        "Critical",
        critical
    )

    c3.metric(
        "Faults",
        faults
    )

    c4.metric(
        "Avg Health",
        health
    )