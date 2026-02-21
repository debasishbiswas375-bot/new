import streamlit as st
import importlib
import os

# ==================================================
# 1. PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Accounting Expert",
    page_icon="logo.png",
    layout="wide"
)

# ==================================================
# 2. SESSION STATE & NAVIGATION
# ==================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# ==================================================
# 3. PAGE LOADER
# ==================================================
def load_page(name):
    try:
        # Dynamically imports from the 'pages' folder
        return importlib.import_module(f"pages.{name}")
    except Exception as e:
        st.error(f"Import error: {e}")
        return None

# ==================================================
# 4. CUSTOM CSS
# ==================================================
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
.brand-text { font-size: 20px; color: #2C3E50; line-height: 1.1; font-weight: 600; }
.menu-label { font-size: 14px; font-weight: 700; color: #5f6368; margin: 15px 0 5px 0; }
div.stButton > button { width: 100%; border-radius: 8px; text-align: left; padding: 8px 12px; border: 1px solid #f0f2f6; background-color: white; color: #5f6368; margin-bottom: 5px; }
div.stButton > button:hover { border-color: #00AEEF; color: #00AEEF; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# 5. SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=70)

    st.markdown('<div class="brand-text">Accounting<br>Expert</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)

    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("📂 Converter"): navigate_to("Converter")
    if st.button("👤 My Profile"): navigate_to("Profile")
    if st.button("🔐 Access Portal"): navigate_to("Auth")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦 Packages", type="primary"): navigate_to("Packages")

# ==================================================
# 6. ROUTING
# ==================================================
current = st.session_state.current_page
page_module = load_page(current)

if page_module and hasattr(page_module, "app"):
    page_module.app()
else:
    st.title(current)
    st.error(f"{current}.py not found in pages folder or is missing 'def app():'")
