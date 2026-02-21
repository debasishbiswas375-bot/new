import streamlit as st
import requests

# IMPORTANT: Check this URL. If you see "No such app" in your browser, 
# you need to update this to your correct Heroku app name.
DJANGO_URL = "https://your-actual-backend.herokuapp.com" 

REGISTER_URL = f"{DJANGO_URL}/register/"
VERIFY_URL = f"{DJANGO_URL}/verify-email/"

def app():
    st.title("Access Portal")
    
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        st.text_input("Username", key="auth_user")
        st.text_input("Password", type="password", key="auth_pass")
        if st.button("Login"):
            st.info("Login logic is currently handled by the backend.")

    with tab2:
        st.subheader("Register")
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

        if len(pin_code) == 6:
            try:
                res = requests.get(f"https://api.postalpincode.in/pincode/{pin_code}")
                data = res.json()
                if data[0]["Status"] == "Success":
                    district = data[0]["PostOffice"][0]["District"]
                    state = data[0]["PostOffice"][0]["State"]
                    st.success(f"Location: {district}, {state}")
            except:
                pass

        if st.button("Register"):
            try:
                response = requests.post(
                    REGISTER_URL,
                    json={
                        "username": new_u, "email": email, "password": new_p,
                        "full_name": full_name, "company": company, "phone": phone,
                        "address": address, "pin_code": pin_code, 
                        "district": district, "state": state
                    }
                )

                # This part prevents the HTML error wall from appearing
                if "application/json" in response.headers.get("Content-Type", ""):
                    st.success(response.json().get("message", "Registration sent!"))
                else:
                    st.error("Error: The backend URL (DJANGO_URL) is incorrect or the Heroku app is not running.")
            except Exception as e:
                st.error(f"Connection failed: {e}")

        st.divider()
        st.subheader("Verify Email")
        otp_user = st.text_input("Username for OTP")
        otp = st.text_input("Enter OTP")

        if st.button("Verify Email"):
            try:
                response = requests.post(VERIFY_URL, json={"username": otp_user, "otp": otp})
                if response.status_code == 200:
                    st.success("Email verified!")
                else:
                    st.error(response.json().get("error", "Invalid OTP"))
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    app()
