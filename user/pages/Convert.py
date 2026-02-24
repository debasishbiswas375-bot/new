import streamlit as st
import requests

DJANGO_API = "https://your-django-domain.com/api/convert/"

st.title("Convert Document")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first.")
    st.stop()

uploaded_file = st.file_uploader("Upload PDF")

if uploaded_file and st.button("Convert (0.10 Credit)"):

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(DJANGO_API, headers=headers)

    st.json(response.json())
