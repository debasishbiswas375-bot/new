import streamlit as st
import importlib

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Accounting Expert", page_icon="📊", layout="wide")

# 2. DYNAMIC MAPPING (Matches your /pages folder)
def load_page(name):
    try:
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

# 4. CUSTOM SIDEBAR STYLE
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e0e0e0; }
        .menu-label { font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 700; color: #2C3E50; margin: 15px 0; padding-left: 10px; }
        div.stButton > button {
            width: 100%; border-radius: 10px; text-align: left; padding: 8px 15px;
            border: 1px solid #f0f2f6; background-color: white; color: #5f6368;
            font-weight: 500; margin-bottom: 8px; transition: all 0.2s ease;
        }
        div.stButton > button:hover { border-color: #00AEEF; color: #00AEEF; background-color: #f0f9ff; }
    </style>
""", unsafe_allow_html=True)

# 5. SIDEBAR MENU
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("logo.png", use_container_width=True)
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)
    
    if st.button("📊  Dashboard"): navigate_to("Dashboard")
    if st.button("☁️  Converter"): navigate_to("Converter")
    if st.button("👤  My Profile"): navigate_to("Profile")
    if st.button("🔐  Login / Register"): navigate_to("Login")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦  Packages", type="primary"): navigate_to("Packages")

# 6. HEADER & CONTENT ROUTING
try:
    from modules import style
    style.apply_global_theme() 
except:
    pass

# FIXED LINE 81: Ensure the syntax is clean
st.markdown("<h2 style='text-align: center;'>Accounting Expert Dashboard</h2>", unsafe_allow_html=True)

page = st.session_state.current_page
if page == "Dashboard" and dashboard_mod:
    dashboard_mod.app()
elif page == "Converter" and converter_mod:
    converter_mod.app()
elif page == "Profile" and profile_mod:
    profile_mod.app()
elif page == "Login" and auth_mod:
    auth_mod.app()

# 7. FOOTER
try:
    style.add_footer()
except:
    pass
