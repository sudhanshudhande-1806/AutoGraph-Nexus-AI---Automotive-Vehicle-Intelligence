import streamlit as st


def render_header(title, subtitle):

    st.markdown(
        f"""
<div style='background:linear-gradient(135deg,#06b6d4,#2563eb,#7c3aed);
padding:30px;
border-radius:24px;
margin-bottom:30px;
box-shadow:0 0 60px rgba(59,130,246,.4);'>

<h1 style='color:white;
margin:0;
font-size:56px;
font-weight:800;'>{title}</h1>

<p style='color:white;
font-size:20px;
margin-top:10px;'>{subtitle}</p>

</div>
""",
        unsafe_allow_html=True
    )