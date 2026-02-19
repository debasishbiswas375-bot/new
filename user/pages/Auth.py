import streamlit as st
import psycopg2
import hashlib
from modules.style import apply_global_theme, add_footer

# Apply the global theme for Accounting Expert
apply_global_theme()

def get_db_connection():
    """Establishes connection to the Neon PostgreSQL database."""
    return psycopg2.connect(st.secrets["DATABASE_URL"])

def hash_pass(password):
    """Creates a SHA256 hash to ensure secure storage and matching."""
    return hashlib.sha256(str.encode(password)).hexdigest()

st.title("🔐 Access Portal")

# Using tabs to separate the forms
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
                # Targeting converter_customuser to match our registration table
                cur.execute("SELECT password FROM converter_customuser WHERE username = %s", (l_user,))
                res = cur.fetchone()
                conn.close()
                
                # Check if user exists and if hashed password matches
                if res and res[0] == hash_pass(l_pass):
                    st.session_state["username"] = l_user
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- FULL REGISTRATION SECTION ---
with tab2:
    st.subheader("Create a New Business Profile")
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            u_reg = st.text_input("Username*")
            p_reg = st.text_input("Password*", type="password")
            fname = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            
        with col2:
            email = st.text_input("Email Address")
            p_conf = st.text_input("Confirm Password*", type="password")
            company = st.text_input("Company Name")
            
        address = st.text_area("Full Business Address")
        
        submit = st.form_submit_button("Register & Sync to Admin")
        
        if submit:
            if p_reg != p_conf:
                st.error("Passwords do not match!")
            elif not u_reg or not p_reg:
                st.warning("Username and Password are required.")
            else:
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    
                    # Step 1: Save details to converter_customuser
                    # We hash the password before saving to prevent plain-text issues
                    cur.execute(
                        """INSERT INTO converter_customuser 
                           (username, password, full_name, email, phone, company, address, is_active, date_joined) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, True, NOW()) RETURNING id""",
                        (u_reg, hash_pass(p_reg), fname, email, phone, company, address)
                    )
                    uid = cur.fetchone()[0]
                    
                    # Step 2: Automatically create the Profile and assign 100 Credits
                    cur.execute("INSERT INTO converter_userprofile (user_id, credits) VALUES (%s, 100)", (uid,))
                    
                    conn.commit()
                    st.success(f"Success! {u_reg} is now registered and synced.")
                    conn.close()
                except Exception as e:
                    st.error(f"Sync failed: {e}")

# Adds the branded footer to the bottom of the page
add_footer() 
