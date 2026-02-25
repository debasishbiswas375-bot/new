import streamlit as st

def app():
    st.title("📊 Accounting Expert Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Credits Available", st.session_state.get("credits", 100))
    col2.metric("Files Converted", "0")
    col3.metric("Current Plan", "Standard Free")

    st.markdown("---")
    st.subheader("📚 Quick Start Topics")
    
    topics = {
        "Accounting Basics": "Introduction to the double-entry system.",
        "Tally Prime Setup": "How to create your first company in Tally."
    }

    for topic, desc in topics.items():
        with st.expander(f"📙 {topic}"):
            st.write(desc)
