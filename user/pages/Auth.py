import streamlit as st
import requests

DJANGO_URL = "https://accountingexpert.onrender.com"

REGISTER_URL = f"{DJANGO_URL}/api/register/"
LOGIN_URL = f"{DJANGO_URL}/api/login/"
USER_INFO_URL = f"{DJANGO_URL}/api/user-info/"
CONVERT_URL = f"{DJANGO_URL}/api/convert/"


def app():
    st.title("🔐 Access Portal")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = requests.post(LOGIN_URL, json={
                "username": username,
                "password": password
            })

            if res.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful")
            else:
                st.error("Invalid credentials")

    # REGISTER
    with tab2:
        new_u = st.text_input("New Username")
        email = st.text_input("Email")
        new_p = st.text_input("New Password", type="password")

        if st.button("Register"):
            res = requests.post(REGISTER_URL, json={
                "username": new_u,
                "password": new_p,
                "email": email
            })

            if res.status_code == 201:
                st.success("Registered successfully")
            else:
                st.error(res.json().get("error"))


# ===============================
# DASHBOARD SECTION
# ===============================
if "logged_in" in st.session_state and st.session_state.logged_in:

    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Choose", ["Dashboard", "Converter", "Plans"])

    username = st.session_state.username

    if menu == "Dashboard":
        res = requests.get(USER_INFO_URL, params={"username": username})
        data = res.json()

        st.header("Dashboard")
        st.metric("Current Plan", data["plan"])
        st.metric("Credits", data["credits"])
        st.metric("Files Converted", data["files_converted"])

    elif menu == "Converter":
        st.header("Convert File")
        if st.button("Convert Dummy File"):
            res = requests.post(CONVERT_URL, data={"username": username})
            st.success(res.json().get("message", res.json().get("error")))

    elif menu == "Plans":
        st.header("Available Plans")
        st.write("Basic – 50 credits")
        st.write("Pro – 200 credits")
        st.write("Enterprise – Custom")


if __name__ == "__main__":
    app()
