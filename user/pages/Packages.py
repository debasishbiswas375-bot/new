import streamlit as st
import requests


API_URL = "https://accountingexpert.onrender.com/plans/"


def app():
    st.title("📦 Point Packages")

    try:
        response = requests.get(API_URL)
        data = response.json()
        plans = data.get("plans", [])

        if not plans:
            st.warning("No plans available.")
            return

        cols = st.columns(3)

        for index, plan in enumerate(plans):
            with cols[index % 3]:

                st.markdown(f"""
                ### {plan['name']}
                
                **{plan['credit_limit']} Points**  
                Duration: {plan['duration_months']} Month(s)  
                
                ₹{plan['price']}
                """)

                if st.button(f"Buy {plan['name']}", key=plan['id']):
                    st.success(f"You selected {plan['name']}")

    except Exception as e:
        st.error("Failed to load plans.")
        st.write(str(e))
