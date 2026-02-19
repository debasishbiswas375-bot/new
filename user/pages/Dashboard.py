import streamlit as st

def app():
    st.title("📚 Learning Hub")
    
    topics = {
        "Accounting Basics": "Introduction to the double-entry system.",
        "Debits and Credits": "The foundation of every transaction.",
        "Accounting Equation": "Assets = Liabilities + Equity",
        "Tally Prime Setup": "How to create your first company in Tally."
    }

    search = st.text_input("Search for a topic...", placeholder="e.g. Debits")

    for topic, desc in topics.items():
        if search.lower() in topic.lower():
            with st.expander(f"📙 {topic}"):
                st.write(desc)
                st.button(f"Read Full Lesson: {topic}", key=topic)
