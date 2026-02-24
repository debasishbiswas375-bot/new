import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .topbar {
        background-color: #f8f9fa;
        padding: 15px;
        font-size: 20px;
        font-weight: bold;
        border-bottom: 1px solid #ddd;
    }

    section[data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: white;
    }

    .stButton button {
        width: 100%;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
