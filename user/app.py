import streamlit as st
import importlib
import os
import sys

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Accounting Expert",
    page_icon="logo.png",
    layout="wide"
)

# --------------------------------------------------
# 2. SESSION STATE NAVIGATION
# --------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page


# --------------------------------------------------
# 3. BULLETPROOF PAGE LOADER (FIXED)
# --------------------------------------------------
def load_page(name):
    try:
        pages_path = os.path.join(os.getcwd(), "pages")

        # Ensure pages folder is in Python path
        if pages_path not in sys.path:
            sys.path.insert(0, pages_path)

        module = importlib.import_module(name)
        return module

    except Exception as e:
        st.error(f"Import error: {e}")
        return None


# --------------------------------------------------
# 4. CUSTOM CSS
# --------------------------------------------------
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

        .menu-label {
            font-family: 'sans-serif';
            font-size: 14px;
            font-weight: 700;
            color: #5f6368;
            margin: 15px 0 5px 0;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            text-align: left;
            padding: 8px 12px;
            border: 1px solid #f0f2f6;
            background-color: white;
            color: #5f6368;
            font-weight: 500;
            margin-bottom: 5px;
        }

        div.stButton > button:hover {
            border-color: #00AEEF;
            color: #00AEEF;
        }
    </style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 5. SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("<br>", unsafe_allow_html=True)

    logo_path = "logo.png"

    col_logo, col_text = st.columns([1, 2.5])

    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=65)

    with col_text:
        st.markdown(
            '<div style="margin-top: 5px;">'
            '<span class="brand-text">Accounting<br>Expert</span>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="menu-label">Main Menu</div>', unsafe_allow_html=True)

    if st.button("📈 Dashboard"):
        navigate_to("Dashboard")

    if st.button("📂 Converter"):
        navigate_to("Converter")

    if st.button("👤 My Profile"):
        navigate_to("Profile")

    if st.button("🔐 Access Portal"):
        navigate_to("Auth")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📦 Packages", type="primary"):
        navigate_to("Packages")


# --------------------------------------------------
# 6. PAGE ROUTING
# --------------------------------------------------
current = st.session_state.current_page
page_module = load_page(current)

if page_module and hasattr(page_module, "app"):
    page_module.app()
else:
    st.title(current)
    st.error(
        f"{current}.py not found in pages folder or is missing 'def app():'"
    )
