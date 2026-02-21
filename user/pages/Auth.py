VERIFY_URL = f"{DJANGO_URL}/verify-email/"

with tab2:

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
                st.success(f"{district}, {state}")
        except:
            pass

    if st.button("Register"):
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

        st.success(response.json().get("message"))

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
            st.success("Email verified successfully!")
        else:
            st.error(response.json().get("error"))
