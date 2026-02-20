import streamlit as st

def app():
    st.title("📦 Point Packages")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### Basic\n50 Points\n₹99")
        st.button("Buy Basic")
    with col2:
        st.success("### Pro\n500 Points\n₹599")
        st.button("Buy Pro", type="primary")
    with col3:
        st.info("### Enterprise\nUnlimited\n₹1999\12 Months")
        st.button("Contact Us")
