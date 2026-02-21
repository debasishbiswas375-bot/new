import streamlit as st
import requests

# Define your backend URL here to fix the "not defined" error
DJANGO_URL = "https://your-django-app-url.herokuapp.com" 
REGISTER_URL = f"{DJANGO_URL}/register/"
VERIFY_URL = f"{DJANGO_URL}/verify-email/"

def app():
    st.title("Access Portal")
    
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to your account")
        # Add your login logic here
        login_user = st.text_input("Username", key="login_u")
        login_pass = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            st.info("Login logic goes here")

    with tab2:
        st.subheader("Create a New Account")
        full_name = st.text_input("Full Name")
        new_u = st.text_input("New Username")
        email = st.text_input("Email")
        new_p = st.text_input("New Password", type="password")

        company = st.text_input("Company (Optional)")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        pin_code = st.text_input("PIN Code")

        district = ""
        state = ""

        # Auto-fetch District and State from PIN
        if len(pin_code) == 6:
            try:
                res = requests.get(f"https://api.postalpincode.in/pincode/{pin_code}")
                data = res.json()
                if data[0]["Status"] == "Success":
                    district = data[0]["PostOffice"][0]["District"]
                    state = data[0]["PostOffice"][0]["State"]
                    st.success(f"Location Found: {district}, {state}")
            except Exception as e:
                pass

        if st.button("Register"):
            try:
                response = requests.post(
                    REGISTER_URL,
                    json={
                        "username": new_u,
                        "email": email,
                        "password": new_p,
                        "full_name": full_name,
                        "company": company,
                        "phone": phone,
                        "address": address,
                        "pin_code": pin_code,
                        "district": district,
                        "state": state,
                    }
                )
                if response.status_code == 201 or response.status_code == 200:
                    st.success(response.json().get("message", "Registration successful!"))
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to server: {e}")

        st.divider()

        st.subheader("Verify Email")
        otp_user = st.text_input("Username for OTP")
        otp = st.text_input("Enter OTP")

        if st.button("Verify Email"):
            try:
                response = requests.post(
                    VERIFY_URL,
                    json={
                        "username": otp_user,
                        "otp": otp
                    }
                )

                if response.status_code == 200:
                    st.success("Email verified successfully!")
                else:
                    st.error(response.json().get("error", "Verification failed"))
            except Exception as e:
                st.error(f"Connection error: {e}")

# This allows you to run the file individually for testing
if __name__ == "__main__":
    app()
