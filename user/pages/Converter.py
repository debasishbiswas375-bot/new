import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

def get_ledger_names(html_file):
    try:
        soup = BeautifulSoup(html_file, 'html.parser')
        ledgers = [td.text.strip() for td in soup.find_all('td') if len(td.text.strip()) > 1]
        return sorted(list(set(ledgers)))
    except Exception:
        return []

def app():
    st.title("🛡️ Accounting Expert | AI Bank")
    st.markdown("##### Turn messy Bank Statements into Tally Vouchers in seconds.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠️ 1. Settings & Mapping")
        master_file = st.file_uploader("Upload Tally Master (Optional)", type="html")
        party_options = get_ledger_names(master_file) if master_file else ["Upload Master.html to see Ledgers"]
        st.selectbox("Select Bank Ledger", ["State Bank of India - 38500202509"])
        st.selectbox("Select Default Party", options=party_options)

    with col2:
        st.subheader("📂 2. Upload & Convert")
        st.selectbox("Select Bank Format", ["SBI", "HDFC", "ICICI"])
        st.file_uploader("Drop your Statement here", type=["xlsx", "xls", "pdf"])
        if st.button("🚀 Start AI Conversion"):
            st.info("Engine active: Processing your statement...")
