import streamlit as st
import requests

API_URL = "https://accountingexpert.onrender.com/plans/"

def app():
    st.title("📦 Point Packages")

    # ===============================
    # Premium Card CSS
    # ===============================
    st.markdown("""
    <style>
    .plan-card {
        padding: 25px;
        border-radius: 18px;
        background: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .plan-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    .plan-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .plan-price {
        font-size: 20px;
        font-weight: bold;
        color: #4F46E5;
        margin-top: 10px;
    }

    .plan-feature {
        font-size: 15px;
        margin-bottom: 5px;
        color: #4B5563;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===============================
    # Fetch Plans from Django API
    # ===============================
    try:
        response = requests.get(API_URL)
        plans = response.json().get("plans", [])

        if not plans:
            st.warning("No plans available.")
            return

        cols = st.columns(3)

        for index, plan in enumerate(plans):
            with cols[index % 3]:

                st.markdown(f"""
                <div class="plan-card">
                    <div class="plan-title">{plan['name']}</div>
                    <div class="plan-feature"><b>{plan['credit_limit']} Points</b></div>
                    <div class="plan-feature">Duration: {plan['duration_months']} Month(s)</div>
                    <div class="plan-price">₹{plan['price']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Buy {plan['name']}", key=plan['id']):
                    st.success(f"You selected {plan['name']}")

    except Exception as e:
        st.error("Failed to load plans.")
        st.write(str(e))
