import streamlit as st
import importlib
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Accounting Expert", page_icon="📈", layout="wide")

# 2. DYNAMIC MAPPING
def load_page(name):
    try:
        # Adjusted for the /user/pages directory structure
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        return None

dashboard_mod = load_page("Dashboard")
converter_mod = load_page("Converter")
profile_mod = load_page("Profile")
auth_mod = load_page("Auth")

# 3. NAVIGATION STATE
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# 4. SIDEBAR MENU (FIXED LOGO PATH)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Path is relative to the repository root
    logo_path = "user/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("Logo missing at user/logo.png")
        
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)
    
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Login / Register"): navigate_to("Login")

# 5. CONTENT ROUTING
page = st.session_state.current_page
if page == "Dashboard" and dashboard_mod:
    dashboard_mod.app()
elif page == "Converter" and converter_mod:
    converter_mod.app()
# ... (add other routing here)
