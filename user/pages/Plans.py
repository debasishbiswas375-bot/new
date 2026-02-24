import streamlit as st

# TITLE + BREADCRUMB
st.markdown('<div class="page-title">Plans</div>', unsafe_allow_html=True)
st.markdown('<div class="breadcrumb">Home › Converter › Plans</div>', unsafe_allow_html=True)

st.write("")

# ADD BUTTON RIGHT SIDE
col1, col2 = st.columns([8,2])
with col2:
    st.button("➕ Add plan")

# TABLE CARD
st.markdown('<div class="admin-card">', unsafe_allow_html=True)

st.table({
    "Name": ["STARTUP PLAN"],
    "Price": ["99.00"],
    "Credit limit": ["50"],
    "Duration months": ["1"]
})

st.markdown('</div>', unsafe_allow_html=True)
