import streamlit as st


def kpi_card(
    title,
    value,
    icon,
    color="#3b82f6"
):

    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:20px;
            padding:25px;
            backdrop-filter:blur(20px);
            box-shadow:0px 0px 25px {color};
            min-height:140px;
        ">

            <h4 style="
                color:white;
                margin-bottom:15px;
                font-size:22px;
            ">
                {icon} {title}
            </h4>

            <h1 style="
                color:white;
                margin:0;
                font-size:48px;
                font-weight:700;
            ">
                {value}
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )