import streamlit as st
import importlib
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Accounting Expert", page_icon="📈", layout="wide")

# 2. NAVIGATION STATE
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# 3. DYNAMIC MAPPING (Targeting the /pages folder)
def load_page(name):
    try:
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        return None

# 4. CUSTOM SIDEBAR STYLE
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        .menu-label { font-family: 'Poppins', sans-serif; font-size: 14px; font-weight: 700; color: #2C3E50; margin: 10px 0; }
        div.stButton > button {
            width: 100%; border-radius: 8px; text-align: left; padding: 5px 10px;
            background-color: white; color: #5f6368; font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# 5. SIDEBAR MENU
with st.sidebar:
    # Use a smaller width for the logo
    logo_path = "user/logo.png" if os.path.exists("user/logo.png") else "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120) # Small logo size
    
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)
    
    # These names MUST match your file names in the /pages folder
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Access Portal"): navigate_to("Auth")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦 Packages", type="primary"): navigate_to("Packages")

# 6. CONTENT ROUTING
current_page = st.session_state.current_page
page_mod = load_page(current_page)

if page_mod and hasattr(page_mod, 'app'):
    page_mod.app()
else:
    st.title(current_page)
    # This error appears if the .py file name doesn't match the button name above
    st.error(f"{current_page}.py not found in pages folder or is missing 'def app():'")
