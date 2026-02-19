import streamlit as st
import hashlib
import psycopg2

def get_db_connection():
    # Ensure DATABASE_URL is in your Streamlit Secrets
    return psycopg2.connect(st.secrets["DATABASE_URL"])

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Register Business"])

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
                    # 1. Sync to Django auth_user table
                    cur.execute(
                        "INSERT INTO auth_user (username, password, email, is_active, is_staff, date_joined) "
                        "VALUES (%s, %s, %s, True, False, NOW()) RETURNING id",
                        (u_reg, hash_pass(p_reg), email)
                    )
                    uid = cur.fetchone()[0]
                    
                    # 2. Sync to custom profiles table using user_id_id
                    cur.execute("INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)", (uid, u_reg, email))
                    
                    conn.commit()
                    st.success(f"Success! {u_reg} is now registered.")
                    conn.close()
                except Exception as e:
                    st.error(f"Sync failed: {e}")
