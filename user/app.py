import streamlit as st
import requests
from supabase import create_client

# =============================
# CONFIG
import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


st.set_page_config(page_title="Accounting Expert", layout="wide")

# =============================
# SESSION
# =============================
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# =============================
# AUTH UI
# =============================
st.title("Accounting Expert")

menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Convert"])

# REGISTER
if menu == "Register":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        st.success("Check your email to verify account.")

# LOGIN
elif menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res.user:
            st.session_state.user = res.user
            st.session_state.token = res.session.access_token
            st.success("Login successful")

# CONVERT
elif menu == "Convert":
    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        uploaded_file = st.file_uploader("Upload PDF")

        if uploaded_file and st.button("Convert (0.10 credit)"):
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            response = requests.post(DJANGO_API, headers=headers)

            st.json(response.json())
