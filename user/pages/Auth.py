import streamlit as st
import hashlib
from database import get_db_connection

def hash_pass(password):
    """Creates a SHA256 hash to ensure secure storage and matching."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    # --- LOGIN SECTION ---
    with tab1:
        st.subheader("Login to your Account")
        with st.form("login_form"):
            l_user = st.text_input("Username")
            l_pass = st.text_input("Password", type="password")
            
            if st.form_submit_button("Sign In"):
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    # Targeting auth_user for Admin compatibility
                    cur.execute("SELECT password, id FROM auth_user WHERE username = %s", (l_user,))
                    res = cur.fetchone()
                    
                    if res and res[0] == hash_pass(l_pass):
                        st.session_state["username"] = l_user
                        st.session_state["user_id"] = res[1]
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password.")
                    conn.close()
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- REGISTRATION SECTION ---
    with tab2:
        st.subheader("Create a New Business Profile")
        with st.form("registration_form"):
            u_reg = st.text_input("Username*")
            p_reg = st.text_input("Password*", type="password")
            email = st.text_input("Email Address")
            submit = st.form_submit_button("Register & Sync to Admin")
            
            if submit:
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    # 1. Save to auth_user for Admin Portal access
                    cur.execute(
                        "INSERT INTO auth_user (username, password, email, is_active, date_joined) "
                        "VALUES (%s, %s, %s, True, NOW()) RETURNING id",
                        (u_reg, hash_pass(p_reg), email)
                    )
                    uid = cur.fetchone()[0]
                    # 2. Create the Profile with 100 default points (using user_id_id column)
                    cur.execute("INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)", (uid, u_reg, email))
                    conn.commit()
                    st.success(f"Success! {u_reg} is now registered.")
                    conn.close()
                except Exception as e:
                    st.error(f"Sync failed: {e}")
