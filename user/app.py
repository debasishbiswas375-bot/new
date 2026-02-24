import streamlit as st
from supabase import create_client

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Accounting Expert",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# JAZZMIN STYLE CSS
# -----------------------------
st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    backdrop-filter: blur(12px);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Main background */
[data-testid="stAppViewContainer"] {
    background-color: #f1f5f9;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SUPABASE INIT
# -----------------------------
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Supabase configuration error.")
    st.stop()

# -----------------------------
# SESSION STATE
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# -----------------------------
# LOGIN PAGE (ONLY ROOT PAGE)
# -----------------------------
st.title("Accounting Expert")

if not st.session_state.user:
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
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

    st.info("After login, use sidebar navigation.")

else:
    st.success("Logged in successfully!")
    st.info("Use sidebar to navigate.")
