import streamlit as st
import os

def apply_global_theme():
    # Fetch from session state or database
    credits = st.session_state.get("credits", 0)
    user_name = st.session_state.get("username", "Guest")

    st.markdown(f"""
        <style>
        .card-credits {{ 
            font-size: 13px; font-weight: 700; color: #1a73e8; 
            background: #e8f0fe; padding: 4px 12px; border-radius: 12px; 
        }}
        </style>
        <div class="floating-top-right">
            <div class="card-credits">Points: {credits}</div>
            <div class="user-name">{user_name}</div>
        </div>
    """, unsafe_allow_html=True)
