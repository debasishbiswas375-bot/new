import streamlit as st

st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="breadcrumb">Home › Dashboard</div>', unsafe_allow_html=True)

st.markdown('<div class="admin-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("Credits Remaining", "50")
col2.metric("Current Plan", "Startup")
col3.metric("Files Converted", "12")

st.markdown('</div>', unsafe_allow_html=True)
