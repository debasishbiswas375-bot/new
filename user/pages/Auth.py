import streamlit as st
import requests

# 🔥 CHANGE THIS TO YOUR RENDER URL
DJANGO_BASE_URL = "https://accountingexpert.onrender.com"

REGISTER_URL = f"{DJANGO_BASE_URL}/api/register/"
LOGIN_URL = f"{DJANGO_BASE_URL}/api/login/"


def register_user(username, email, password):
    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    response = requests.post(REGISTER_URL, json=payload)

    if response.status_code == 201:
        return True, "Registration successful"
    else:
        return False, response.json().get("error", "Registration failed")


def login_user(username, password):
    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(LOGIN_URL, json=payload)

    if response.status_code == 200:
        return True, "Login successful"
    else:
        return False, response.json().get("error", "Invalid credentials")


def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    # LOGIN
    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            success, message = login_user(username, password)

            if success:
                st.success(message)
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error(message)

    # REGISTER
    with tab2:
        st.subheader("Register Business")

        with st.form("registration_form"):
            new_u = st.text_input("Username*")
            email = st.text_input("Email")
            new_p = st.text_input("Password*", type="password")

            if st.form_submit_button("Register & Sync"):
                success, message = register_user(new_u, email, new_p)

                if success:
                    st.success(message)
                else:
                    st.error(message)


if __name__ == "__main__":
    app()
