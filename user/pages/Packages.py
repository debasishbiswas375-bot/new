import streamlit as st
import requests

API_URL = "https://accountingexpert.onrender.com/plans/"


def app():
    st.title("📦 Point Packages")

    try:
        response = requests.get(API_URL)
        plans = response.json().get("plans", [])

        cols = st.columns(3)

        for index, plan in enumerate(plans):
            with cols[index % 3]:

                card_text = f"""
### {plan['name']}

**{plan['credit_limit']} Points**  
Duration: {plan['duration_months']} Month(s)  

₹{plan['price']}
"""

                # Alternate card colors
                if index % 2 == 0:
                    st.info(card_text)
                else:
                    st.success(card_text)

                if st.button(f"Buy {plan['name']}", key=plan['id']):
                    st.success(f"You selected {plan['name']}")

    except:
        st.error("Failed to load plans.")
