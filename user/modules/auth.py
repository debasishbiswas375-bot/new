import streamlit as st
from database import get_db_connection
import hashlib

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Register Business"])

    with tab2:
        with st.form("registration"):
            u = st.text_input("Username*")
            p = st.text_input("Password*", type="password")
            e = st.text_input("Email")
            if st.form_submit_button("Register"):
                conn = get_db_connection()
                cur = conn.cursor()
                try:
                    # Sync to auth_user for Admin Login
                    cur.execute(
                        "INSERT INTO auth_user (username, password, email, is_active, is_staff, is_superuser, date_joined) "
                        "VALUES (%s, %s, %s, True, False, False, NOW()) RETURNING id",
                        (u, hash_pass(p), e)
                    )
                    uid = cur.fetchone()[0]
                    # Sync to profiles for Credits/Points using the correct user_id_id column
                    cur.execute("INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)", (uid, u, e))
                    conn.commit()
                    st.success("Business Registered! You can now log in.")
                except Exception as ex:
                    st.error(f"Sync failed: {ex}")
                finally:
                    conn.close()
