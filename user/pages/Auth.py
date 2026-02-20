import streamlit as st
import hashlib
import psycopg2

def app():
    st.title("🔐 Access Portal")
    
    # Create the tabs
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    # --- TAB 1: SIGN IN ---
    with tab1:
        st.subheader("Login to your Account")
        with st.form("login_form"):
            login_user = st.text_input("Username")
            login_pw = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Sign In")

            if submit_login:
                try:
                    # Connect using the secret URL (ensure you removed the [] brackets in Secrets!)
                    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                    cur = conn.cursor()
                    
                    # Query to match your auth_user table
                    cur.execute("SELECT id FROM auth_user WHERE username = %s AND password = %s", (login_user, login_pw))
                    user = cur.fetchone()
                    
                    if user:
                        st.success(f"Welcome back, {login_user}!")
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = login_user
                    else:
                        st.error("Invalid username or password.")
                    
                    conn.close()
                except Exception as ex:
                    st.error(f"Login failed: {ex}")

    # --- TAB 2: REGISTRATION ---
    with tab2:
        st.subheader("Register Business")
        with st.form("reg_form"):
            u = st.text_input("Username*")
            e = st.text_input("Email")
            p = st.text_input("Password*", type="password")
            
            if st.form_submit_button("Register & Sync"):
                if not u or not p:
                    st.warning("Please fill in required fields (*)")
                else:
                    try:
                        conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                        cur = conn.cursor()
                        
                        # 1. Insert into auth_user
                        cur.execute(
                            "INSERT INTO auth_user (username, password, email, is_active, date_joined) "
                            "VALUES (%s, %s, %s, True, NOW()) RETURNING id", 
                            (u, p, e)
                        )
                        uid = cur.fetchone()[0]
                        
                        # 2. Insert into profiles using the returned ID
                        cur.execute(
                            "INSERT INTO profiles (user_id_id, username, email, points) "
                            "VALUES (%s, %s, %s, 100)", 
                            (uid, u, e)
                        )
                        
                        conn.commit()
                        st.success(f"Success! {u} registered.")
                        conn.close()
                    except Exception as ex:
                        st.error(f"Sync failed: {ex}")

# This tells Streamlit to run the app function when the page is selected
if __name__ == "__main__":
    app()
