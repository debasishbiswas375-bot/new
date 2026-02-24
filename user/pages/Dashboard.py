import streamlit as st

st.title("Dashboard")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.metric("Credits Remaining", "50")

with col2:
    st.metric("Plan", "Startup")

st.write("Welcome,", st.session_state.user.email)
