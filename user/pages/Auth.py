import streamlit as st
import psycopg2
import hashlib

def get_db_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Register"])

    with tab2:
        with st.form("reg_form"):
            u = st.text_input("Username*")
            p = st.text_input("Password*", type="password")
            e = st.text_input("Email")
            if st.form_submit_button("Create Business Account"):
                conn = get_db_connection()
                cur = conn.cursor()
                try:
                    # 1. Insert into Django auth_user
                    cur.execute(
                        "INSERT INTO auth_user (username, password, email, is_active, is_staff, is_superuser, date_joined) "
                        "VALUES (%s, %s, %s, True, False, False, NOW()) RETURNING id",
                        (u, hash_pass(p), e)
                    )
                    uid = cur.fetchone()[0]
                    # 2. Insert into profiles using the CORRECT Django column: user_id_id
                    cur.execute(
                        "INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)",
                        (uid, u, e)
                    )
                    conn.commit()
                    st.success("Registration Successful! Account synced to Admin.")
                except Exception as ex:
                    st.error(f"Sync failed: {ex}")
                finally:
                    conn.close()
