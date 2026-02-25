import streamlit as st

def app():
    st.title("🛡️ AI Bank Converter")
    st.markdown("##### Upload your bank statement to begin conversion.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠️ Settings")
        st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI"])
        st.file_uploader("Upload Tally Master (HTML)", type="html")
    
    with col2:
        st.subheader("📂 Upload")
        st.file_uploader("Drop Statement (PDF/Excel)", type=["pdf", "xlsx", "xls"])
        if st.button("🚀 Start Conversion"):
            st.info("AI Engine processing...")
