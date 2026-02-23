import streamlit as st

def app():
    st.title("👤 My Profile")
    if "username" in st.session_state:
        st.write(f"**Username:** {st.session_state['username']}")
        st.write(f"**Current Points:** {st.session_state.get('credits', 100)}")
    else:
        st.warning("Please log in to view your profile details.")
