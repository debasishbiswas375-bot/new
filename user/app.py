import streamlit as st
import importlib
import os

st.set_page_config(page_title="Accounting Expert", page_icon="📈", layout="wide")

# FIX: Dynamic mapping adjusted for subdirectory structure
def load_page(name):
    try:
        # Streamlit on Cloud often needs the full path from the repo root
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        try:
            return importlib.import_module(f"user.pages.{name}")
        except ImportError:
            return None

# NAVIGATION STATE
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# SIDEBAR (FIXED LOGO AND PATHS)
with st.sidebar:
    logo_path = "user/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("Logo missing")
    
    if st.button("📊 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Access Portal"): navigate_to("Auth")

# CONTENT ROUTING
page = st.session_state.current_page
mod = load_page(page)

if mod and hasattr(mod, 'app'):
    mod.app()
else:
    st.error(f"{page}.py file not found in pages directory.")
