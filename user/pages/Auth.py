import streamlit as st
import requests

# ===============================
# DJANGO BACKEND URL
# ===============================
DJANGO_URL = "https://accountingexpert.onrender.com"

REGISTER_URL = f"{DJANGO_URL}/register/"
LOGIN_URL = f"{DJANGO_URL}/login/"


def safe_json(response):
    """
    Safely return JSON if possible,
    otherwise return raw text.
    """
    try:
        return response.json()
    except:
        return {"error": response.text}


def app():
    st.title("🔐 Access Portal")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ==================================================
    # LOGIN SECTION
    # ==================================================
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            if not username or not password:
                st.warning("Please fill all fields.")
                return

            try:
                response = requests.post(
                    LOGIN_URL,
                    json={
                        "username": username,
                        "password": password
                    },
                    timeout=10
                )

                st.write("Status Code:", response.status_code)

                data = safe_json(response)

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful ✅")

                else:
                    st.error(data.get("error", "Login failed"))

            except Exception as e:
                st.error(f"Connection Error: {e}")

    # ==================================================
    # REGISTER SECTION
    # ==================================================
    with tab2:
        new_u = st.text_input("New Username", key="reg_user")
        email = st.text_input("Email", key="reg_email")
        new_p = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):

            if not new_u or not email or not new_p:
                st.warning("Please fill all fields.")
                return

            try:
                response = requests.post(
                    REGISTER_URL,
                    json={
                        "username": new_u,
                        "email": email,
                        "password": new_p
                    },
                    timeout=10
                )

                st.write("Status Code:", response.status_code)
                st.write("Raw Response:", response.text)

                data = safe_json(response)

                if response.status_code in [200, 201]:
                    st.success("Registered successfully! Please login. ✅")

                else:
                    st.error(data.get("error", "Registration failed"))

            except Exception as e:
                st.error(f"Connection Error: {e}")


# ==================================================
# DASHBOARD AFTER LOGIN
# ==================================================
if "logged_in" in st.session_state and st.session_state.logged_in:

    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Choose", ["Dashboard"])

    username = st.session_state.username

    if menu == "Dashboard":
        st.header("Welcome 🎉")
        st.write(f"Logged in as: **{username}**")


if __name__ == "__main__":
    app()
