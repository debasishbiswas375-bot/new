import streamlit as st
import hashlib
# Make sure to import your connection function
# from database import get_db_connection 

def app():
    st.title("🔐 Access Portal")
    tab1, tab2 = st.tabs(["Sign In", "Full Business Registration"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login"):
            st.text_input("Username")
            st.text_input("Password", type="password")
            st.form_submit_button("Sign In")
            
    with tab2:
        st.subheader("Register")
        with st.form("reg"):
            st.text_input("Business Name")
            st.text_input("Email")
            st.form_submit_button("Register & Sync")
