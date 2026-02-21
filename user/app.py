import streamlit as st
import importlib
import os

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Accounting Expert",
    page_icon="logo.png",
    layout="wide"
)

# ======================================
# SESSION STATE
# ======================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

def navigate_to(page):
    st.session_state.current_page = page

# ======================================
# PAGE LOADER
# ======================================
def load_page(name):
    try:
        return importlib.import_module(f"pages.{name}")
    except Exception as e:
        st.error(f"Import error: {e}")
        return None

# ======================================
# SIDEBAR
# ======================================
with st.sidebar:

    if os.path.exists("logo.png"):
        st.image("logo.png", width=70)

    st.markdown("### Accounting Expert")

    if st.button("📈 Dashboard"):
        navigate_to("Dashboard")

    if st.button("📂 Converter"):
        navigate_to("Converter")

    if st.button("👤 Profile"):
        navigate_to("Profile")

    if st.button("🔐 Access Portal"):
        navigate_to("Auth")

    if st.button("📦 Packages"):
        navigate_to("Packages")

# ======================================
# ROUTING
# ======================================
current = st.session_state.current_page
page_module = load_page(current)

if page_module and hasattr(page_module, "app"):
    page_module.app()
else:
    st.title(current)
    st.error(f"{current}.py not found in pages folder or missing 'def app()'")
