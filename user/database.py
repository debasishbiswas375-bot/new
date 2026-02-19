import streamlit as st
from supabase import create_client, Client
import psycopg2

# Supabase Credentials
SUPABASE_URL = "https://aombczanizdhiulwkuhf.supabase.co"
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "Deba9002043666") 

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db_connection():
    """Establishes connection to the Supabase PostgreSQL database."""
    # Ensure this secret is added in your Streamlit Cloud settings
    return psycopg2.connect(st.secrets["DATABASE_URL"])
