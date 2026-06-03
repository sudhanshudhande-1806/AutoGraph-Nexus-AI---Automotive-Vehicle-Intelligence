import streamlit as st


def load_theme():

    st.markdown(
        """
        <style>

        .stApp{
            background:
            radial-gradient(
                circle at top,
                #020617,
                #0b1120,
                #000000
            );
        }

        section[data-testid="stSidebar"]{
            background:
            linear-gradient(
                180deg,
                #111827,
                #030712
            );
        }

        div[data-testid="metric-container"]{
            background:rgba(255,255,255,0.05);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:20px;
            padding:20px;
            backdrop-filter:blur(12px);
            box-shadow:0 0 25px rgba(59,130,246,0.15);
        }

        div[data-testid="metric-container"]:hover{
            transform:translateY(-3px);
            transition:0.3s;
            box-shadow:0 0 35px rgba(59,130,246,0.4);
        }

        h1,h2,h3{
            color:white !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )