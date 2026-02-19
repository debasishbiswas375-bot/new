import streamlit as st
import importlib
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Accounting Expert", page_icon="logo.png", layout="wide")

# 2. NAVIGATION STATE
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# 3. DYNAMIC MAPPING
def load_page(name):
    try:
        # Matches the files in your /pages folder exactly
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        return None

# 4. CUSTOM CSS (STYLISH FONT & SIDEBAR)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&display=swap');
        
        [data-testid="stSidebarNav"] { display: none; }
        
        .brand-text {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #2C3E50;
            line-height: 1.1;
            font-style: italic;
            font-weight: 600;
        }
        
        .menu-label { font-family: 'sans-serif'; font-size: 14px; font-weight: 700; color: #5f6368; margin: 15px 0 5px 0; }
        
        div.stButton > button {
            width: 100%; border-radius: 8px; text-align: left; padding: 8px 12px;
            border: 1px solid #f0f2f6; background-color: white; color: #5f6368;
            font-weight: 500; margin-bottom: 5px;
        }
        div.stButton > button:hover { border-color: #00AEEF; color: #00AEEF; }
    </style>
""", unsafe_allow_html=True)

# 5. SIDEBAR BRANDING & MENU
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Side-by-Side Logo and Stylish Name
    logo_path = "user/logo.png" if os.path.exists("user/logo.png") else "logo.png"
    col_logo, col_text = st.columns([1, 2.5])
    
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=65)
    with col_text:
        # Places "Accounting Expert" in the marked area
        st.markdown('<div style="margin-top: 5px;"><span class="brand-text">Accounting<br>Expert</span></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)
    
    # Navigation Buttons (Must match filenames in /pages folder)
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Access Portal"): navigate_to("Auth")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦 Packages", type="primary"): navigate_to("Packages")

# 6. CONTENT ROUTING
current = st.session_state.current_page
page_mod = load_page(current)

if page_mod and hasattr(page_mod, 'app'):
    page_mod.app()
else:
    st.title(current)
    # Shown if Converter.py, Profile.py, Auth.py, or Packages.py are missing or named wrong
    st.error(f"{current}.py not found in pages folder or is missing 'def app():'")

# 7. FOOTER / THEME (Optional)
try:
    from modules import style
    style.apply_global_theme() 
except:
    pass
