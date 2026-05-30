import base64
from io import BytesIO

import streamlit as st
from PIL import Image


def configure_page():
    try:
        icon_img = Image.open("./src/images/icon.png")
        st.set_page_config(
            page_title="KeepIn - Platform Loker",
            page_icon=icon_img,
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except Exception:
        st.set_page_config(
            page_title="KeepIn - Platform Loker",
            layout="wide",
            initial_sidebar_state="collapsed",
        )


def init_session_state():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"

    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None

    if "active_menu" not in st.session_state:
        st.session_state["active_menu"] = "Beranda"

    if "id_user" not in st.session_state:
        st.session_state["id_user"] = None


def image_to_base64(img_path):
    try:
        img = Image.open(img_path)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception:
        return None


def get_logo_html():
    logo_base64 = image_to_base64("./src/images/logo.png")
    return f'<img src="data:image/png;base64,{logo_base64}" width="30">' if logo_base64 else "🟢"


def render_global_css():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; }
        .welcome-title { font-size: 32px; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
        .welcome-subtitle { font-size: 14px; color: #64748B; line-height: 1.5; margin-bottom: 30px; }
        .form-label { font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; margin-top: 15px; }
        .right-title { font-size: 42px; font-weight: 800; color: #0F172A; line-height: 1.2; }
        .highlight-text { color: #52D1A2; }
        .right-subtitle { font-size: 16px; color: #475569; margin-top: 20px; margin-bottom: 40px; }
        .feature-box { display: flex; align-items: flex-start; margin-bottom: 25px; }
        .feature-icon-1 { background-color: #E6F9F2; padding: 10px; border-radius: 10px; margin-right: 15px; }
        .feature-icon-2 { background-color: #EEF2FF; padding: 10px; border-radius: 10px; margin-right: 15px; }
        .feature-icon-3 { background-color: #FFF7ED; padding: 10px; border-radius: 10px; margin-right: 15px; }
        .feature-title { font-size: 15px; font-weight: 700; color: #1E293B; }
        .feature-desc { font-size: 13px; color: #64748B; margin-top: 2px; }
        
        /* Tombol Utama */
        div.row-widget.stButton > button { width: 100%; background-color: #52D1A2; color: white; font-weight: 600; padding: 12px; border-radius: 8px; border: none; margin-top: 20px; }
        div.row-widget.stButton > button:hover { background-color: #3cb88a; color: white; }
        
        /* Tombol Hitam Khusus Login */
        div.login-btn-container button { background-color: #1E293B !important; }
        div.login-btn-container button:hover { background-color: #0F172A !important; }
        </style>
    """, unsafe_allow_html=True)
