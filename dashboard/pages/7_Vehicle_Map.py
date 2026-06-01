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

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar

render_sidebar()

st.title("📍 Live Vehicle Map")

df = pd.read_csv(
    "data/vehicle_locations.csv"
)

st.map(
    df.rename(
        columns={
            "lat":"latitude",
            "lon":"longitude"
        }
    )
)

st.dataframe(df)