import streamlit as st
import importlib
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Accounting Expert", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. NAVIGATION STATE MANAGEMENT
# This ensures the app remembers which page you are on when it reruns
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# 3. DYNAMIC MODULE LOADER
def load_page(name):
    try:
        # This targets the .py files inside your 'user/pages/' folder
        return importlib.import_module(f"pages.{name}")
    except ImportError:
        return None

# 4. CUSTOM SIDEBAR AND BUTTON STYLING (CSS)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        .menu-label { 
            font-family: 'Poppins', sans-serif; 
            font-size: 16px; 
            font-weight: 700; 
            color: #2C3E50; 
            margin: 15px 0; 
            padding-left: 10px; 
        }
        div.stButton > button {
            width: 100%; border-radius: 10px; text-align: left; padding: 8px 15px;
            border: 1px solid #f0f2f6; background-color: white; color: #5f6368;
            font-weight: 500; margin-bottom: 8px; transition: all 0.2s ease;
        }
        div.stButton > button:hover { 
            border-color: #00AEEF; 
            color: #00AEEF; 
            background-color: #f0f9ff; 
        }
    </style>
""", unsafe_allow_html=True)

# 5. SIDEBAR NAVIGATION MENU
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secure logo loading: Checks multiple paths to ensure it doesn't crash
    logo_paths = ["user/logo.png", "logo.png", "user/logo 1.png"]
    found_logo = False
    for path in logo_paths:
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            found_logo = True
            break
    if not found_logo:
        st.warning("Logo missing")
        
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)
    
    # NAVIGATION BUTTONS
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Access Portal"): navigate_to("Auth")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦 Packages", type="primary"): navigate_to("Packages")

# 6. CONTENT ROUTING LOGIC
# This section renders the content of the selected page
current = st.session_state.current_page
page_mod = load_page(current)

if page_mod and hasattr(page_mod, 'app'):
    # Run the app() function inside the specific page file (e.g., Dashboard.py)
    page_mod.app()
else:
    # Fallback error if a file is missing or improperly coded
    st.title(current)
    st.error(f"Error: {current}.py not found in 'pages' folder or is missing the 'def app():' function.")

# 7. OPTIONAL GLOBAL STYLING
try:
    from modules import style
    style.apply_global_theme() 
except ImportError:
    pass
