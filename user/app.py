import streamlit as st
from supabase import create_client

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Accounting Expert",
    layout="wide",
)

# --------------------------------------------------
# SUPABASE
# --------------------------------------------------
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
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

# --------------------------------------------------
# MAIN CONTENT (ALWAYS VISIBLE)
# --------------------------------------------------
st.title("Dashboard")

col1, col2, col3 = st.columns(3)

if st.session_state.user:
    credits = "48"
    plan = "Startup"
else:
    credits = "Demo"
    plan = "Free Preview"

col1.metric("Credits Remaining", credits)
col2.metric("Current Plan", plan)
col3.metric("Files Converted", "12" if st.session_state.user else "Preview Only")

st.divider()

# --------------------------------------------------
# FEATURE SECTION
# --------------------------------------------------
st.subheader("Document Conversion")

uploaded = st.file_uploader("Upload PDF")

if not st.session_state.user:
    st.info("🔒 Login required for full access.")
else:
    if uploaded and st.button("Convert (0.10 Credit)"):
        st.success("Conversion started...")
