import streamlit as st

def render_sidebar():

    st.sidebar.title(
        "🚗 AutoGraph Nexus AI"
    )

    st.sidebar.success(
        "Fleet Command Center"
    )

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
        Connected Vehicle Platform

        • Fleet Health

        • Fault Analytics

        • AI Copilot

        • Knowledge Graph

        • Maintenance Queue
        """
    )