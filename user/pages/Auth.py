import streamlit as st
import requests
import os

# ======================================
# LOAD DJANGO BACKEND URL
# ======================================
DJANGO_URL = os.getenv("DJANGO_URL")

if not DJANGO_URL:
    st.error("❌ DJANGO_URL not set in Streamlit Secrets.")
    st.stop()

REGISTER_URL = f"{DJANGO_URL}/register/"
VERIFY_URL = f"{DJANGO_URL}/verify-email/"
LOGIN_URL = f"{DJANGO_URL}/login/"

# ======================================
# MAIN FUNCTION
# ======================================
def app():

    st.title("🔐 Access Portal")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ==============================
    # LOGIN
    # ==============================
    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            response = requests.post(
                LOGIN_URL,
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200:
                st.success("✅ Login successful")
            else:
                st.error(response.json().get("error", "Login failed"))

    # ==============================
    # REGISTER
    # ==============================
    with tab2:

        full_name = st.text_input("Full Name")
        new_username = st.text_input("New Username")
        email = st.text_input("Email")
        new_password = st.text_input("New Password", type="password")

        company = st.text_input("Company (Optional)")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        pin_code = st.text_input("PIN Code")

        district = ""
        state = ""

        # Auto fetch district/state
        if len(pin_code) == 6:
            try:
                res = requests.get(
                    f"https://api.postalpincode.in/pincode/{pin_code}"
                )
                data = res.json()

                if data[0]["Status"] == "Success":
                    district = data[0]["PostOffice"][0]["District"]
                    state = data[0]["PostOffice"][0]["State"]
                    st.success(f"{district}, {state}")

            except:
                pass

        if st.button("Register"):
            response = requests.post(
                REGISTER_URL,
                json={
                    "username": new_username,
                    "email": email,
                    "password": new_password,
                    "full_name": full_name,
                    "company": company,
                    "phone": phone,
                    "address": address,
                    "pin_code": pin_code,
                    "district": district,
                    "state": state,
                }
            )

            if response.status_code == 200:
                st.success(response.json().get("message", "Registered!"))
            else:
                st.error(response.json().get("error", "Registration failed"))

        st.divider()
        st.subheader("Verify Email")

        otp_user = st.text_input("Username for OTP")
        otp = st.text_input("Enter OTP")

        if st.button("Verify Email"):
            response = requests.post(
                VERIFY_URL,
                json={
                    "username": otp_user,
                    "otp": otp
                }
            )

            if response.status_code == 200:
                st.success("✅ Email verified successfully!")
            else:
                st.error(response.json().get("error", "Verification failed"))
