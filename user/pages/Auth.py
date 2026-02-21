import streamlit as st
import importlib
import os

# ==================================================
# 1. PAGE CONFIG (FIXED SYNTAX)
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

def load_page(name):
    try:
        return importlib.import_module(f"pages.{name}")
    except Exception as e:
        st.error(f"Import error: {e}")
        return None

# ==================================================
# 3. SIDEBAR & ROUTING
# ==================================================
with st.sidebar:
    st.title("Accounting Expert")
    if st.button("📈 Dashboard"): navigate_to("Dashboard")
    if st.button("🔐 Access Portal"): navigate_to("Auth")

current = st.session_state.current_page
page_module = load_page(current)

if page_module and hasattr(page_module, "app"):
    page_module.app()
else:
    st.error(f"Could not load page: {current}")
