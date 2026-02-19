import streamlit as st
from database import get_db_connection

def app():
    st.title("👤 My Business Profile")
    
    if "username" not in st.session_state:
        st.warning("Please log in through the Access Portal to view your profile.")
        return

    user = st.session_state["username"]
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Fetch profile data synced from Admin
        cur.execute("SELECT email, points, plan_id FROM profiles WHERE username = %s", (user,))
        data = cur.fetchone()
        conn.close()

        if data:
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Username:** {user}")
                st.info(f"**Email:** {data[0]}")
            with col2:
                st.success(f"**Current Points:** {data[1]}")
                st.success(f"**Account Level:** {data[2] if data[2] else 'Free'}")
        else:
            st.error("Profile record not found. Please contact support.")
            
    except Exception as e:
        st.error(f"Error loading profile: {e}")
