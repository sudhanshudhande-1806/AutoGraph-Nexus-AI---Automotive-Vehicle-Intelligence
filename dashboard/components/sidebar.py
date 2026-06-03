import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            # 🚗 AutoGraph Nexus AI
            """
        )

        st.success(
            "Fleet Command Center"
        )

        st.markdown("---")

        st.info(
            """
            Connected Vehicle Platform

            • Fleet Health

            • Fault Analytics

            • AI Copilot

            • Knowledge Graph

            • Predictive Maintenance
            """
        )