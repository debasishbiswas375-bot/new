import streamlit as st

st.set_page_config(layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>

body {
    background-color: #f4f6f9;
}

.block-container {
    padding-top: 0.5rem;
    max-width: 1400px;
}

/* Sidebar */
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

/* Active menu */
.active-menu {
    background-color: #007bff;
    padding: 8px;
    border-radius: 5px;
    color: white !important;
}

/* Topbar */
.topbar {
    background: white;
    padding: 15px 25px;
    border-bottom: 1px solid #dee2e6;
    margin-bottom: 25px;
}

/* Page title */
.page-title {
    font-size: 26px;
    font-weight: 600;
}

/* Breadcrumb */
.breadcrumb {
    color: #6c757d;
    font-size: 14px;
    margin-top: 5px;
}

/* Card */
.admin-card {
    background: white;
    border-radius: 6px;
    padding: 20px;
    border: 1px solid #dee2e6;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #28a745;
    color: white;
    border-radius: 5px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Django administration</div>', unsafe_allow_html=True)

    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"

    if st.button("Plans"):
        st.session_state.page = "Plans"

# ---------------- TOPBAR ----------------
st.markdown("""
<div class="topbar">
    ☰
    <span style="float:right;">Logout</span>
</div>
""", unsafe_allow_html=True)

# ---------------- ROUTING ----------------
if st.session_state.page == "Dashboard":

    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home › Dashboard</div>', unsafe_allow_html=True)

    st.markdown('<div class="admin-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Credits Remaining", "50")
    col2.metric("Current Plan", "Startup")
    col3.metric("Files Converted", "12")

    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.page == "Plans":

    st.markdown('<div class="page-title">Plans</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home › Converter › Plans</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([8,2])
    with col2:
        st.button("➕ Add plan")

    st.markdown('<div class="admin-card">', unsafe_allow_html=True)

    st.table({
        "Name": ["STARTUP PLAN"],
        "Price": ["99.00"],
        "Credit limit": ["50"],
        "Duration months": ["1"]
    })

    st.markdown('</div>', unsafe_allow_html=True)
