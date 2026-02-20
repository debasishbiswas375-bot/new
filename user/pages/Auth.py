import streamlit as st
import psycopg2
import hashlib

st.set_page_config(page_title="Access Portal")

st.title("🔐 Access Portal")

tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])


# ------------------------
# SIGN IN
# ------------------------
with tab1:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            conn = psycopg2.connect(st.secrets["DATABASE_URL"])
            cur = conn.cursor()

            # Hash password (basic example)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cur.execute(
                "SELECT * FROM auth_user WHERE username=%s AND password=%s",
                (username, hashed_password),
            )

            user = cur.fetchone()

            if user:
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

            conn.close()

        except Exception as e:
            st.error(f"Database error: {e}")


# ------------------------
# REGISTRATION
# ------------------------
with tab2:
    st.subheader("Register Business")

    with st.form("reg_form"):
        u = st.text_input("Username*")
        e = st.text_input("Email")
        p = st.text_input("Password*", type="password")

        submitted = st.form_submit_button("Register & Sync")

        if submitted:
            try:
                conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                cur = conn.cursor()

                hashed_password = hashlib.sha256(p.encode()).hexdigest()

                cur.execute(
                    """
                    INSERT INTO auth_user 
                    (username, password, email, is_active, date_joined)
                    VALUES (%s, %s, %s, True, NOW()) 
                    RETURNING id
                    """,
                    (u, hashed_password, e),
                )

                uid = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO profiles 
                    (user_id_id, username, email, points)
                    VALUES (%s, %s, %s, 100)
                    """,
                    (uid, u, e),
                )

                conn.commit()
                conn.close()

                st.success(f"Success! {u} registered.")

            except Exception as ex:
                st.error(f"Registration failed: {ex}")
