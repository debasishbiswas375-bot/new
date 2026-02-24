import streamlit as st

st.title("Profile")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    st.stop()

st.write("Email:", st.session_state.user.email)

if st.button("Logout"):
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()
