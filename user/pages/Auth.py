import streamlit as st
import psycopg2

def app():
    st.title("🔐 Access Portal")
    
    # Matching the tabs in your logic
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])

    with tab1:
        st.subheader("Login to your Account")
        with st.form("login_form"):
            login_user = st.text_input("Username")
            login_pw = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Sign In")

            if submit_login:
                try:
                    # Connection string from st.secrets
                    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
                    cur = conn.cursor()
                    
                    # Checking the auth_user table
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
                    st.error(f"Database connection failed: {ex}")

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
                        
                        # Insert into auth_user
                        cur.execute(
                            "INSERT INTO auth_user (username, password, email, is_active, date_joined) "
                            "VALUES (%s, %s, %s, True, NOW()) RETURNING id", 
                            (u, p, e)
                        )
                        uid = cur.fetchone()[0]
                        
                        # Insert into profiles
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

# This line is CRITICAL for the router to find the page
if __name__ == "__main__":
    app()
