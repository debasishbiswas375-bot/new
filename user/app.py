import streamlit as st
import os
import importlib.util
from style import load_css

st.set_page_config(layout="wide")
load_css()

PAGES_DIR = "pages"

# Get all page files
page_files = [
    f for f in os.listdir(PAGES_DIR)
    if f.endswith(".py") and not f.startswith("_")
]

# Sort naturally (1_, 2_, 3_)
page_files.sort()

def clean_name(filename):
    name = filename.replace(".py", "")
    
    # Remove number prefix like 1_, 2_, 10_
    if "_" in name and name.split("_")[0].isdigit():
        name = name.split("_", 1)[1]
    
    return name

# Build page dictionary
pages = {}
for file in page_files:
    clean = clean_name(file)
    pages[clean] = file

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## Django administration")

    if "page" not in st.session_state:
        st.session_state.page = list(pages.keys())[0]

    for display_name in pages:
        if st.button(display_name, key=display_name):
            st.session_state.page = display_name

# ---------------- TOPBAR ----------------
st.markdown("""
<div class="topbar">
    Django administration
    <span style="float:right;">Logout</span>
</div>
""", unsafe_allow_html=True)

# ---------------- PAGE LOADER ----------------
selected_file = pages[st.session_state.page]
page_path = os.path.join(PAGES_DIR, selected_file)

spec = importlib.util.spec_from_file_location("page", page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
