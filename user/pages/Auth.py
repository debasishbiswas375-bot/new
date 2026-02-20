import streamlit as st
import psycopg2
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    # LOGIN SECTION
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            try:
                conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                cur = conn.cursor()
                hashed = hash_password(password)
                
                cur.execute("SELECT id FROM auth_user WHERE username = %s AND password = %s", (username, hashed))
                user = cur.fetchone()

                if user:
                    st.success("✅ Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                else:
                    st.error("❌ Invalid username or password")
                conn.close()
            except Exception as e:
                st.error(f"Database error: {e}")

    # REGISTRATION SECTION
    with tab2:
        st.subheader("Register Business")
        with st.form("registration_form"):
            new_u = st.text_input("Username*", key="reg_user")
            email = st.text_input("Email", key="reg_email")
            new_p = st.text_input("Password*", type="password", key="reg_pass")
            if st.form_submit_button("Register & Sync"):
                try:
                    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                    cur = conn.cursor()
                    hashed = hash_password(new_p)

                    cur.execute("INSERT INTO auth_user (username, password, email, is_active, date_joined) VALUES (%s, %s, %s, TRUE, NOW()) RETURNING id", (new_u, hashed, email))
                    user_id = cur.fetchone()[0]

                    cur.execute("INSERT INTO profiles (user_id_id, username, email, points) VALUES (%s, %s, %s, 100)", (user_id, new_u, email))
                    
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 {new_u} registered successfully!")
                except Exception as ex:
                    st.error(f"Registration failed: {ex}")

if __name__ == "__main__":
    app()
