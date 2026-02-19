import streamlit as st
import importlib

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Accounting Expert",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. DYNAMIC PAGE LOADING (The Fix for 03_Account.py)
# -----------------------------------------------------------------------------
# We create a dictionary to hold our page modules
pages = {}

# Try to load Dashboard
try:
    pages["Dashboard"] = importlib.import_module("dashboard")
except ImportError:
    pass # We will handle missing files later

# Try to load Converter
try:
    pages["Converter"] = importlib.import_module("converter")
except ImportError:
    pass

# Try to load Packages
try:
    pages["Packages"] = importlib.import_module("packages")
except ImportError:
    pass

# Try to load Profile (specifically pages/03_Account.py)
try:
    # This maps 'pages/03_Account.py' to the key 'Profile'
    pages["Profile"] = importlib.import_module("pages.03_Account")
except ImportError:
    pass


# -----------------------------------------------------------------------------
# 3. CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
        
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap');
        
        .sidebar-title {
            font-family: 'Poppins', sans-serif;
            font-size: 22px;
            font-weight: 700;
            color: #2C3E50;
            margin-top: 10px;
            margin-bottom: 20px;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            text-align: left;
            padding-left: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. NAVIGATION STATE
# -----------------------------------------------------------------------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# -----------------------------------------------------------------------------
# 5. SIDEBAR MENU
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image("logo.png", width=130)
    except:
        st.warning("Logo missing")

    st.markdown('<div class="sidebar-title">Accounting Expert</div>', unsafe_allow_html=True)
    
    if st.button("📊  Dashboard", use_container_width=True):
        navigate_to("Dashboard")
        
    if st.button("☁️  Converter", use_container_width=True):
        navigate_to("Converter")
        
    if st.button("👤  My Profile", use_container_width=True):
        navigate_to("Profile")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📦  Packages", type="primary", use_container_width=True):
        navigate_to("Packages")

# -----------------------------------------------------------------------------
# 6. MAIN CONTENT ROUTING
# -----------------------------------------------------------------------------
page = st.session_state.current_page

if page == "Dashboard":
    if "Dashboard" in pages:
        pages["Dashboard"].app()
    else:
        st.title("Dashboard")
        st.write("Dashboard.py file not found.")

elif page == "Converter":
    if "Converter" in pages:
        pages["Converter"].app()
    else:
        st.title("Converter")
        st.write("Converter.py file not found.")

elif page == "Profile":
    if "Profile" in pages:
        pages["Profile"].app() # This runs 03_Account.py
    else:
        st.title("My Profile")
        st.error("Could not find 'pages/03_Account.py'")

elif page == "Packages":
    if "Packages" in pages:
        pages["Packages"].app()
    else:
        st.title("Packages")
        st.write("Packages.py file not found.")
