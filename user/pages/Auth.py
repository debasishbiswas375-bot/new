import streamlit as st
import requests

# REPLACEME: Use your actual Heroku app URL here
DJANGO_URL = "https://your-actual-backend-app.herokuapp.com" 

# Endpoints
REGISTER_URL = f"{DJANGO_URL}/register/"
VERIFY_URL = f"{DJANGO_URL}/verify-email/"

def app():
    st.title("Access Portal")
    
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        st.text_input("Username", key="l_user")
        st.text_input("Password", type="password", key="l_pass")
        if st.button("Sign In"):
            st.warning("Login functionality needs to be implemented in the backend.")

    with tab2:
        st.subheader("Create Account")
        
        # Form Fields
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name")
            new_u = st.text_input("New Username")
            email = st.text_input("Email")
            new_p = st.text_input("New Password", type="password")
        
        with col2:
            company = st.text_input("Company (Optional)")
            phone = st.text_input("Phone Number")
            pin_code = st.text_input("PIN Code", max_chars=6)
            address = st.text_area("Address", height=68)

        district = ""
        state = ""

        # Auto-fetch Location from PIN
        if len(pin_code) == 6:
            try:
                res = requests.get(f"https://api.postalpincode.in/pincode/{pin_code}")
                data = res.json()
                if data[0]["Status"] == "Success":
                    district = data[0]["PostOffice"][0]["District"]
                    state = data[0]["PostOffice"][0]["State"]
                    st.success(f"📍 {district}, {state}")
            except:
                pass

        if st.button("Register Now"):
            payload = {
                "username": new_u, "email": email, "password": new_p,
                "full_name": full_name, "company": company, "phone": phone,
                "address": address, "pin_code": pin_code, "district": district, "state": state
            }
            
            try:
                response = requests.post(REGISTER_URL, json=payload)
                
                # Check if we got JSON back (prevents the HTML 'No such app' error)
                if "application/json" in response.headers.get("Content-Type", ""):
                    data = response.json()
                    if response.status_code == 201 or response.status_code == 200:
                        st.success(data.get("message", "Registration successful! Check your email."))
                    else:
                        st.error(data.get("error", "Registration failed."))
                else:
                    st.error("Backend Error: The DJANGO_URL might be incorrect or the server is down.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

        st.divider()

        st.subheader("Verify Email")
        otp_user = st.text_input("Username", key="v_user")
        otp = st.text_input("Enter OTP", key="v_otp")

        if st.button("Verify"):
            try:
                response = requests.post(VERIFY_URL, json={"username": otp_user, "otp": otp})
                if response.status_code == 200:
                    st.success("Email verified successfully!")
                else:
                    st.error(response.json().get("error", "Invalid OTP"))
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    app()
