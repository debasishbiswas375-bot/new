import streamlit as st
import hashlib
import psycopg2

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    with tab2:
        st.subheader("Register")
        with st.form("reg_form"):
            u = st.text_input("Business Name")
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            
            if st.form_submit_button("Register & Sync"):
                try:
                    # This uses the secret you added in Step 1
                    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                    cur = conn.cursor()
                    
                    # 1. Create the main login account
                    cur.execute(
                        "INSERT INTO auth_user (username, password, email, is_active, date_joined) "
                        "VALUES (%s, %s, %s, True, NOW()) RETURNING id",
                        (u, hash_pass(p), e)
                    )
                    uid = cur.fetchone()[0]
                    
                    # 2. Create the profile with 100 points
                    cur.execute(
                        "INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)",
                        (uid, u, e)
                    )
                    conn.commit()
                    st.success(f"Success! {u} is now registered and synced to Admin.")
                    conn.close()
                except Exception as ex:
                    st.error(f"Sync failed: {ex}")
