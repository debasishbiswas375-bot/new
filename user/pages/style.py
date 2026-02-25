import streamlit as st
import os

def apply_global_theme():
    user_name = st.session_state.get("username", "Guest")
    credits = st.session_state.get("credits", 0)

    st.markdown(f"""
        <style>
        header {{visibility: hidden;}}
        .floating-top-right {{
            position: fixed; top: 15px; right: 25px; z-index: 9999;
            display: flex; align-items: center; gap: 12px;
        }}
        .google-ring {{
            width: 40px; height: 40px; border-radius: 50%; padding: 2px;
            background: conic-gradient(#4285F4, #34A853, #FBBC05, #EA4335);
        }}
        .user-avatar {{ width: 100%; height: 100%; border-radius: 50%; background: white; }}
        </style>
        <div class="floating-top-right">
            <div class="google-ring"><div class="user-avatar"></div></div>
            <div style="font-weight: bold;">{user_name} (Points: {credits})</div>
        </div>
    """, unsafe_allow_html=True)
