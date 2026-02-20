import streamlit as st
import requests

DJANGO_URL = "https://accountingexpert.onrender.com"

REGISTER_URL = f"{DJANGO_URL}/register/"
LOGIN_URL = f"{DJANGO_URL}/login/"


def app():
    st.title("🔐 Access Portal")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ===============================
    # LOGIN
    # ===============================
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            try:
                res = requests.post(
                    LOGIN_URL,
                    json={
                        "username": username,
                        "password": password
                    },
                    timeout=10
                )

                if res.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful")
                else:
                    try:
                        st.error(res.json().get("error", "Invalid credentials"))
                    except:
                        st.error("Login failed")

            except Exception as e:
                st.error(f"Error: {e}")

    # ===============================
    # REGISTER
    # ===============================
    with tab2:
        new_u = st.text_input("New Username", key="reg_user")
        email = st.text_input("Email", key="reg_email")
        new_p = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            try:
                res = requests.post(
                    REGISTER_URL,
                    json={
                        "username": new_u,
                        "password": new_p,
                        "email": email
                    },
                    timeout=10
                )

                if res.status_code == 200:
                    st.success("Registered successfully! Please login.")
                else:
                    try:
                        st.error(res.json().get("error", "Registration failed"))
                    except:
                        st.error("Registration failed")

            except Exception as e:
                st.error(f"Error: {e}")


# ===============================
# DASHBOARD SECTION
# ===============================
if "logged_in" in st.session_state and st.session_state.logged_in:

    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Choose", ["Dashboard"])

    username = st.session_state.username

    if menu == "Dashboard":
        st.header("Welcome")
        st.write(f"Logged in as: **{username}**")


if __name__ == "__main__":
    app()
