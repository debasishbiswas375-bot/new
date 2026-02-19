import psycopg2
import streamlit as st

def get_db_connection():
    """Establishes connection to the Supabase PostgreSQL database."""
    # This expects a secret named DATABASE_URL in your Streamlit dashboard
    return psycopg2.connect(st.secrets["DATABASE_URL"])
