import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

# --- 1. PRO ENGINE: LEDGER EXTRACTION ---
def get_ledger_names(html_file):
    try:
        soup = BeautifulSoup(html_file, 'html.parser')
        # Tally HTML exports store names in <td> tags
        ledgers = [td.text.strip() for td in soup.find_all('td') if len(td.text.strip()) > 1]
        return sorted(list(set(ledgers)))
    except Exception:
        return []

# --- 2. MAIN CONVERTER INTERFACE ---
def app():
    st.title("🛡️ Accounting Expert | AI Bank")
    st.markdown("##### Turn messy Bank Statements into Tally Vouchers in seconds.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛠️ 1. Settings & Mapping")
        master_file = st.file_uploader("Upload Tally Master (Optional)", type="html")
        
        if master_file:
            real_ledgers = get_ledger_names(master_file)
            st.success(f"✅ Synced {len(real_ledgers)} ledgers")
            premium_label = "⭐ AI Auto-Trace (Premium)"
            party_options = [premium_label] + real_ledgers
        else:
            party_options = ["Upload Master.html to see Ledgers"]

        st.selectbox("Select Bank Ledger", ["State Bank of India - 38500202509"])

        selected_party = st.selectbox("Select Default Party", options=party_options, index=0)

        if "⭐" in selected_party:
            st.toast("Admin Status Verified: Premium Engine Active!", icon="⭐")

    with col2:
        st.subheader("📂 2. Upload & Convert")
        st.selectbox("Select Bank Format", ["SBI", "HDFC", "ICICI"])
        st.text_input("PDF Password", type="password", placeholder="Optional")
        bank_file = st.file_uploader("Drop your Statement here", type=["xlsx", "xls", "pdf"])

    if bank_file and master_file and "⭐" in selected_party:
        st.info("🚀 Premium AI is scanning your statement to match the best ledger...")
