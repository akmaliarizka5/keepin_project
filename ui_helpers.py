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
    defaults = {
        "current_page": "login",
        "user_role": None,
        "user_email": None,
        "active_menu": "Beranda",
        "id_user": None,
        "mitra_register_step": 1,
        "mitra_usaha_form": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
    return f'<img src="data:image/png;base64,{logo_base64}" width="30">' if logo_base64 else "KeepIn"


def render_global_css():
    st.markdown("""
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        fontFamily: { sans: ['Inter', 'ui-sans-serif', 'system-ui'] },
                        colors: {
                            keepin: {
                                ink: '#18181B',
                                muted: '#71717A',
                                emerald: '#10B981',
                                indigo: '#4F46E5',
                                cloud: '#FAFAFA'
                            }
                        }
                    }
                }
            }
        </script>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
        :root {
            --ink:#18181B;
            --muted:#71717A;
            --line:#E5E7EB;
            --surface:#FFFFFF;
            --bg:#FAFAFA;
            --green:#10B981;
            --indigo:#4F46E5;
            --dark:#18181B;
        }
        html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(250,250,250,.78); backdrop-filter: blur(18px); }
        [data-testid="stToolbar"], .stDeployButton { display:none !important; }
        #MainMenu, footer { visibility:hidden; }
        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 30% 0%, rgba(16,185,129,.10), transparent 28%),
                linear-gradient(180deg, #FFFFFF 0%, #FBFCFD 100%);
            border-right: 1px solid #E5E7EB;
            box-shadow: 18px 0 50px rgba(24,24,27,.04);
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding: 30px 20px; }
        [data-testid="stSidebar"] div[role="radiogroup"] label { border-radius: 8px; padding: 8px 10px; margin-bottom: 6px; }
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background: #F2F6FA; border: 1px solid #E4EAF2; }
        .block-container { padding-top: 32px; padding-left: 42px; padding-right: 42px; max-width: 1720px; }
        .welcome-title { font-size: clamp(34px, 3.4vw, 54px); font-weight: 900; color: var(--ink); margin-bottom: 8px; letter-spacing: -.045em; }
        .welcome-subtitle { font-size: 14px; color: #607086; line-height: 1.6; margin-bottom: 30px; }
        .form-label { font-size: 11px; font-weight: 800; color: #90A1B8; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px; margin-top: 15px; }
        .right-title { font-size: 42px; font-weight: 900; color: #0F172A; line-height: 1.12; }
        .highlight-text { color: #62D7B1; }
        .right-subtitle { font-size: 16px; color: #607086; margin-top: 20px; margin-bottom: 40px; }
        .feature-box { display: flex; align-items: flex-start; margin-bottom: 25px; }
        .feature-icon-1, .feature-icon-2, .feature-icon-3 { width: 42px; height: 42px; border-radius: 8px; margin-right: 15px; }
        .feature-icon-1 { background-color: #E6F9F2; }
        .feature-icon-2 { background-color: #EEF2FF; }
        .feature-icon-3 { background-color: #FFF7ED; }
        .feature-title { font-size: 15px; font-weight: 800; color: #1E293B; }
        .feature-desc { font-size: 13px; color: #64748B; margin-top: 2px; }
        div.row-widget.stButton > button { width: 100%; background: linear-gradient(135deg, #10B981, #14B8A6); color: white; font-weight: 800; padding: 12px 16px; border-radius: 12px; border: none; margin-top: 8px; box-shadow: 0 14px 34px rgba(16,185,129,.22); transition: transform .18s ease, box-shadow .18s ease, filter .18s ease; }
        div.row-widget.stButton > button:hover { filter: brightness(.98); color: white; transform: translateY(-1px); box-shadow: 0 20px 46px rgba(16,185,129,.28); }
        [data-testid="stSidebar"] div.row-widget.stButton > button {
            background: transparent;
            color: #52525B;
            box-shadow: none;
            border: 1px solid transparent;
            text-align: left;
            justify-content: flex-start;
            font-weight: 800;
            padding: 12px 14px;
            margin: 4px 0;
            border-radius: 14px;
            min-height: 44px;
            letter-spacing: 0;
        }
        [data-testid="stSidebar"] div.row-widget.stButton > button:hover {
            background: #F8FAFC;
            color: #18181B;
            border-color: #DDE7F0;
            transform: translateX(2px);
        }
        [data-testid="stSidebar"] div.row-widget.stButton > button p {
            font-size: 13px;
            line-height: 1.1;
        }
        div.login-btn-container button { background-color: #1E293B !important; }
        div.login-btn-container button:hover { background-color: #0F172A !important; }
        .k-topbar {
            display:flex;
            justify-content:space-between;
            align-items:center;
            min-height: 58px;
            margin: -6px 0 16px;
        }
        .k-profile-preview {
            display:flex;
            align-items:center;
            justify-content:flex-end;
            gap:10px;
            text-decoration:none !important;
            color:inherit !important;
            padding:8px 10px;
            border-radius: 999px;
            border:1px solid transparent;
            transition: transform .18s ease, background .18s ease, border-color .18s ease, box-shadow .18s ease;
        }
        .k-profile-preview:hover {
            background:#FFFFFF;
            border-color:#E5E7EB;
            box-shadow:0 16px 44px rgba(24,24,27,.08);
            transform: translateY(-1px);
        }
        .k-user-mini { font-size:12px; color:#162235; font-weight:800; text-align:right; line-height:1.15; }
        .k-user-mini span { color:#94A3B8; font-size:10px; letter-spacing:.7px; }
        .k-avatar, .k-avatar-sm, .k-avatar-xl {
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius: 999px;
            color:#064E3B;
            background: linear-gradient(135deg, #D1FAE5, #CCFBF1);
            border: 1px solid #A7F3D0;
            box-shadow: 0 12px 30px rgba(16,185,129,.18);
            font-weight:900;
        }
        .k-avatar { width:42px; height:42px; font-size:13px; }
        .k-avatar-sm { width:38px; height:38px; font-size:12px; flex:0 0 auto; }
        .k-avatar-xl { width:88px; height:88px; font-size:28px; box-shadow: 0 22px 60px rgba(16,185,129,.24); }
        .k-role-pill { display:inline-block; background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; padding:4px 9px; border-radius:999px; font-size:10px; font-weight:900; text-transform:uppercase; }
        .k-card { background:#FFFFFF; border:1px solid #E5E7EB; border-radius:20px; box-shadow:0 18px 60px rgba(24,24,27,.06); padding:26px; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
        .k-card:hover { transform: translateY(-2px); box-shadow:0 26px 76px rgba(24,24,27,.10); border-color:#D4D4D8; }
        .k-card-soft { background:#FFFFFF; border:1px solid #E5E7EB; border-radius:18px; padding:24px; box-shadow:0 14px 46px rgba(24,24,27,.045); }
        .k-muted { color:#8EA0B7; font-size:12px; font-weight:700; }
        .k-section-label { color:#9BAEC7; font-size:11px; font-weight:900; letter-spacing:1.6px; text-transform:uppercase; margin:22px 0 12px; }
        .k-hero-dark { background:linear-gradient(135deg,#18181B 0%,#27272A 58%,#064E3B 100%); color:white; border-radius:28px; padding:48px; box-shadow:0 34px 90px rgba(24,24,27,.22); }
        .k-hero-dark h2 { color:white; font-size:34px; line-height:1.1; margin:0 0 16px; }
        .k-hero-dark p { color:#B9C6D6; max-width:520px; }
        .k-stat .value { font-size:30px; font-weight:900; color:#1E293B; }
        .k-stat .label { color:#94A3B8; font-size:11px; text-transform:uppercase; letter-spacing:1.2px; font-weight:900; }
        .k-chip { display:inline-block; background:#F2F6FA; border:1px solid #E2E8F0; color:#607086; border-radius:999px; padding:6px 10px; font-size:11px; font-weight:800; }
        .k-chip-green { background:#ECFDF5; color:#059669; border-color:#A7F3D0; }
        .k-chip-purple { background:#EEF2FF; color:#4F46E5; border-color:#C7D2FE; }
        .k-shell {
            position: relative;
            overflow: hidden;
            border-radius: 30px;
            padding: 42px;
            background:
                radial-gradient(circle at 86% 12%, rgba(16,185,129,.26), transparent 28%),
                radial-gradient(circle at 28% -6%, rgba(79,70,229,.22), transparent 34%),
                linear-gradient(135deg, #18181B 0%, #27272A 52%, #064E3B 100%);
            color: white;
            box-shadow: 0 34px 110px rgba(24,24,27,.25);
        }
        .k-shell h1 {
            color: white;
            font-size: clamp(42px, 5vw, 72px);
            line-height: .95;
            margin: 14px 0;
            letter-spacing: -.05em;
            max-width: 760px;
        }
        .k-shell p { color: #B9C6D6; font-size: 16px; max-width: 620px; }
        .k-hero-grid { display:grid; grid-template-columns: 1.5fr .9fr; gap: 22px; align-items: stretch; }
        .k-glass {
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 22px;
            padding: 22px;
            backdrop-filter: blur(18px);
        }
        .k-glass strong { color:white; font-size: 26px; }
        .k-action-grid { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
        .k-action-card {
            background: white;
            border: 1px solid #E7ECF3;
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 18px 50px rgba(24,24,27,.06);
            transition: transform .16s ease, box-shadow .16s ease;
        }
        .k-action-card:hover { transform: translateY(-3px); box-shadow: 0 24px 70px rgba(17,24,39,.10); }
        .k-icon {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#EAF9F4;
            color:#35B896;
            font-weight:900;
            margin-bottom: 16px;
        }
        .k-dashboard-grid { display:grid; grid-template-columns: 1.15fr .85fr; gap: 18px; }
        .k-mini-row {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding: 16px 0;
            border-bottom: 1px solid #EEF2F7;
        }
        .k-mini-row:last-child { border-bottom: 0; }
        .k-sidebar-brand {
            display:flex;
            align-items:center;
            gap:10px;
            margin: 8px 0 20px;
        }
        .k-sidebar-logo img { width: 34px; height: 34px; border-radius: 11px; box-shadow: 0 10px 24px rgba(16,185,129,.18); }
        .k-sidebar-title { font-size:20px; font-weight:900; color:#18181B; letter-spacing:-.03em; line-height:1; }
        .k-sidebar-caption { font-size:10px; color:#94A3B8; font-weight:800; margin-top:4px; }
        .k-sidebar-user {
            display:flex;
            align-items:center;
            gap:11px;
            background:#FFFFFF;
            color:#18181B;
            border:1px solid #E5E7EB;
            padding:11px;
            border-radius:18px;
            box-shadow: 0 14px 40px rgba(24,24,27,.045);
            margin: 18px 0 28px;
        }
        .k-sidebar-user-copy { min-width:0; display:flex; flex-direction:column; gap:2px; }
        .k-sidebar-user-copy b { font-size:13px; line-height:1.1; color:#18181B; }
        .k-sidebar-user-copy span {
            color:#71717A;
            font-size:11px;
            overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;
            max-width:165px;
        }
        .k-sidebar-spacer { height:42px; }
        .k-nav-active {
            display:flex;
            align-items:center;
            gap:10px;
            background: linear-gradient(135deg, #ECFDF5, #EEF2FF);
            border: 1px solid #A7F3D0;
            color:#18181B;
            border-radius: 16px;
            padding: 12px 14px;
            font-size: 13px;
            font-weight: 900;
            margin: 4px 0 8px;
            box-shadow: 0 14px 36px rgba(16,185,129,.14);
        }
        .k-nav-active span {
            width:24px;
            height:24px;
            border-radius:9px;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            background:#FFFFFF;
            color:#10B981;
            box-shadow: 0 6px 14px rgba(16,185,129,.14);
        }
        .k-profile-hero {
            position: relative;
            overflow:hidden;
            border-radius: 28px;
            background: #FFFFFF;
            border:1px solid #E5E7EB;
            box-shadow:0 24px 80px rgba(24,24,27,.07);
            margin-bottom: 20px;
        }
        .k-profile-cover {
            height: 130px;
            background:
                radial-gradient(circle at 85% 20%, rgba(16,185,129,.32), transparent 26%),
                radial-gradient(circle at 18% 12%, rgba(79,70,229,.22), transparent 30%),
                linear-gradient(135deg, #18181B 0%, #27272A 55%, #064E3B 100%);
        }
        .k-profile-main {
            display:flex;
            align-items:center;
            gap:18px;
            padding: 0 28px 28px;
            margin-top: -44px;
        }
        .k-profile-main h1 {
            margin: 10px 0 2px;
            font-size: 34px;
            line-height:1;
            color:#18181B;
            letter-spacing:-.04em;
        }
        .k-profile-main p { margin:0; color:#71717A; font-weight:700; }
        .k-orb-card {
            min-height: 210px;
            border-radius: 24px;
            background:
                radial-gradient(circle at 75% 30%, rgba(16,185,129,.18), transparent 28%),
                linear-gradient(135deg,#FFFFFF,#F8FAFC);
            border:1px solid #E5E7EB;
            padding:24px;
            box-shadow:0 18px 50px rgba(24,24,27,.06);
        }
        .stTextInput div[data-baseweb="input"], .stTextArea textarea, .stNumberInput input {
            border-radius: 14px !important;
            border-color: #E5E7EB !important;
            background: #FFFFFF !important;
            box-shadow: 0 8px 24px rgba(24,24,27,.035);
        }
        .stSelectbox div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            border-color: #E5E7EB !important;
        }
        @media (max-width: 980px) {
            .k-hero-grid, .k-action-grid, .k-dashboard-grid { grid-template-columns: 1fr; }
            .block-container { padding-left: 20px; padding-right: 20px; }
        }
        input, textarea, select { border-radius: 8px !important; }
        </style>
    """, unsafe_allow_html=True)
