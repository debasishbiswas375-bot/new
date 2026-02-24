import streamlit as st

st.set_page_config(layout="wide")

# ---------------- JAZZMIN CSS ----------------
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
body {
    background-color: #f4f6f9;
}

/* REMOVE DEFAULT PADDING */
.block-container {
    padding-top: 0.5rem;
    max-width: 1400px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #343a40;
    width: 230px !important;
}

[data-testid="stSidebar"] * {
    color: #c2c7d0 !important;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 600;
    padding: 15px;
    color: white;
}

/* ACTIVE PAGE */
.css-1d391kg {
    background-color: #007bff !important;
}

/* TOP NAVBAR */
.topbar {
    background: white;
    padding: 15px 25px;
    border-bottom: 1px solid #dee2e6;
    margin-bottom: 25px;
}

/* PAGE TITLE */
.page-title {
    font-size: 26px;
    font-weight: 600;
}

/* BREADCRUMB */
.breadcrumb {
    color: #6c757d;
    font-size: 14px;
    margin-top: 5px;
}

/* ADMIN CARD */
.admin-card {
    background: white;
    border-radius: 6px;
    padding: 20px;
    border: 1px solid #dee2e6;
    margin-bottom: 20px;
}

/* GREEN BUTTON */
.stButton>button {
    background-color: #28a745;
    color: white;
    border-radius: 5px;
    border: none;
}

.stButton>button:hover {
    background-color: #218838;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Django administration</div>', unsafe_allow_html=True)
    st.page_link("pages/Dashboard.py", label="Dashboard")
    st.page_link("pages/Plans.py", label="Plans")

# ---------------- TOPBAR ----------------
st.markdown("""
<div class="topbar">
    <span style="font-size:18px;">☰</span>
    <span style="float:right;">Logout</span>
</div>
""", unsafe_allow_html=True)
