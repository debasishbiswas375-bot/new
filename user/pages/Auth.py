import streamlit as st
from database import get_db_connection
import hashlib

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

st.title("🔐 Access Portal")
tab1, tab2 = st.tabs(["Sign In", "Register Business"])

with tab2:
    with st.form("reg_form"):
        u_reg = st.text_input("Username*")
        p_reg = st.text_input("Password*", type="password")
        email = st.text_input("Email")
        
        if st.form_submit_button("Register"):
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                # 1. Insert into Django's user table
                cur.execute(
                    "INSERT INTO auth_user (username, password, email, is_active, is_staff, date_joined) "
                    "VALUES (%s, %s, %s, True, False, NOW()) RETURNING id",
                    (u_reg, hash_pass(p_reg), email)
                )
                uid = cur.fetchone()[0]
                
                # 2. Insert into the custom profiles table we just fixed
                cur.execute(
                    "INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)",
                    (uid, u_reg, email)
                )
                conn.commit()
                st.success("Registration complete! You can now log in.")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()
