import streamlit as st
import base64
import os

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_global_theme():
    # 1. RETRIEVE USER DATA FROM SESSION STATE
    user_name = st.session_state.get("username", "Guest")
    full_name = st.session_state.get("full_name", "Guest User")
    user_email = st.session_state.get("email", "guest@accountingexpert.com")
    credits = st.session_state.get("credits", 0)
    
    # Profile Image Logic
    user_img_base64 = get_base64_image("user_profile.png")
    img_html = f'src="data:image/png;base64,{user_img_base64}"' if user_img_base64 else 'src="https://www.w3schools.com/howto/img_avatar.png"'

    st.markdown(f"""
        <style>
        header {{visibility: hidden;}}
        .floating-top-right {{
            position: fixed; top: 15px; right: 25px; z-index: 999999;
            display: flex; align-items: center; gap: 12px;
        }}
        
        .profile-wrapper {{ position: relative; cursor: pointer; }}
        
        /* Google Ring */
        .google-ring {{
            width: 40px; height: 40px; border-radius: 50%; padding: 2.5px;
            background: conic-gradient(#4285F4 0% 25%, #34A853 25% 50%, #FBBC05 50% 75%, #EA4335 75% 100%);
            display: flex; justify-content: center; align-items: center;
        }}
        .user-avatar {{ width: 100%; height: 100%; border-radius: 50%; background: white; border: 2px solid white; object-fit: cover; }}

        /* Dropdown Card */
        .account-card {{
            display: none; position: absolute; top: 50px; right: 0;
            width: 320px; background-color: #f7f9fc; border-radius: 28px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 20px;
            flex-direction: column; align-items: center; z-index: 1000001;
            border: 1px solid #e0e0e0; font-family: 'Roboto', sans-serif;
        }}
        .profile-wrapper:hover .account-card {{ display: flex; }}
        
        .card-avatar-large {{ width: 70px; height: 70px; border-radius: 50%; margin-bottom: 10px; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .card-fullname {{ font-size: 18px; font-weight: 500; color: #202124; margin-bottom: 2px; }}
        .card-email {{ font-size: 14px; color: #5f6368; margin-bottom: 8px; }}
        .card-credits {{ font-size: 13px; font-weight: 700; color: #1a73e8; background: #e8f0fe; padding: 4px 12px; border-radius: 12px; margin-bottom: 15px; }}
        
        .card-actions {{ width: 100%; display: flex; flex-direction: column; gap: 8px; border-top: 1px solid #e0e0e0; padding-top: 15px; }}
        
        .action-link {{
            text-decoration: none; color: #3c4043; font-size: 14px; font-weight: 500;
            padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #dadce0; background: white;
        }}
        .action-link:hover {{ background-color: #f1f3f4; }}
        
        .logout-btn {{ color: #d93025; border: 1px solid #f5c2c7; }}
        </style>

        <div class="floating-top-right">
            <svg width="24" height="24" fill="#5f6368"><path d="M6,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM6,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM12,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM16,6c0,1.1 0.9,2 2,2s2,-0.9 2,-2 -0.9,-2 -2,-2 -2,0.9 -2,2zM12,8c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,14c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2zM18,20c1.1,0 2,-0.9 2,-2s-0.9,-2 -2,-2 -2,0.9 -2,2 0.9,2 2,2z"></path></svg>
            <div class="profile-wrapper">
                <div class="google-ring"><img {img_html} class="user-avatar"></div>
                <div class="account-card">
                    <img {img_html} class="card-avatar-large">
                    <div class="card-fullname">{full_name}</div>
                    <div class="card-email">{user_email}</div>
                    <div class="card-credits">Credits: {credits}</div>
                    <div class="card-actions">
                        <a href="?page=Profile" class="action-link">Manage your Account</a>
                        <a href="?logout=true" class="action-link logout-btn">Sign out</a>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
