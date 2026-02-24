import streamlit as st
from supabase import create_client

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Accounting Expert",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# JAZZMIN STYLE CSS
# ------------------------------------------------
st.markdown("""
<style>

/* Remove Streamlit top space */
.block-container {
    padding-top: 1.5rem;
    max-width: 1200px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #2c3e50;
    color: white;
}

[data-testid="stSidebar"] * {
    color: #ecf0f1 !important;
}

/* Top Navbar */
.top-navbar {
    background: white;
    padding: 15px 25px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 25px;
    border-radius: 8px;
}

/* Admin Cards */
.admin-card {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Section title */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
}

/* Buttons */
.stButton>button {
    background-color: #1abc9c;
    color: white;
    border-radius: 6px;
    border: none;
}

.stButton>button:hover {
    background-color: #16a085;
}

body {
    background-color: #ecf0f5;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SUPABASE INIT
# ------------------------------------------------
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# ------------------------------------------------
# SIDEBAR CONTENT (Jazzmin Style)
# ------------------------------------------------
with st.sidebar:
    st.title("Accounting Expert")

    if st.session_state.user:
        st.success("Logged in")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.token = None
            st.rerun()
    else:
        st.warning("Demo Mode")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if supabase:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if res.user:
                    st.session_state.user = res.user
                    st.session_state.token = res.session.access_token
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Supabase not configured")

# ------------------------------------------------
# TOP NAVBAR
# ------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <strong>Django Administration</strong>
</div>
""", unsafe_allow_html=True)

st.write("Use sidebar to navigate.")
