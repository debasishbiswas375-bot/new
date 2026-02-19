import streamlit as st
import importlib
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Accounting Expert", page_icon="📈", layout="wide")

# 2. DYNAMIC MAPPING (Corrected for your folder structure)
def load_page(name):
    try:
        # This targets the files inside your 'pages' folder directly
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        return None

# 3. NAVIGATION STATE
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# 4. SIDEBAR MENU (Fixed Logo Path)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    # Check both potential paths for the logo
    logo_path = "user/logo.png" if os.path.exists("user/logo.png") else "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("Logo missing")
        
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Login / Register"): navigate_to("Auth")

# 5. CONTENT ROUTING
page_mod = load_page(st.session_state.current_page)
if page_mod and hasattr(page_mod, 'app'):
    page_mod.app()
else:
    st.error(f"{st.session_state.current_page}.py not found in pages folder.")
