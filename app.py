import streamlit as st
import pandas as pd
import requests
import datetime
from PIL import Image

# --- 1. SET CONFIG ---
icon_gambar = Image.open("./src/images/logo.png")
st.set_page_config(
    page_title="KeepIn Partner Console",
    page_icon=icon_gambar,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS FOR MAJESTIC & BOLD BRANDING (Matching React Preview) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset & Base */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    [data-testid="stSidebar"] { background-color: #1F2937 !important; color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #FFFFFF; }
    
    /* Typography */
    h1, h2, h3, .brand-font {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.04em !important;
    }
    
    p, span, label, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
    }

    /* Custom Header Branding */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 3rem;
    }
    .brand-logo {
        background-color: #10B981;
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 22px;
    }
    .brand-name {
        font-weight: 800;
        font-size: 28px;
        color: #1F2937;
    }

    /* Auth Layout Containers */
    .auth-form-container {
        padding: 10vh 8vw;
        max-width: 650px;
        margin-left: auto;
    }

    /* Bento Cards */
    .bento-card {
        background: white;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .bento-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #10B981;
    }
    
    .metric-label {
        font-size: 13px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
    }

    /* Forms & Inputs */
    div[data-testid="stTextInput"] label p {
        font-weight: 700 !important;
        color: #0F172A !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 16px !important;
        border: 2px solid #F1F5F9 !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        background-color: #F8FAFC !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #10B981 !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 16px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s !important;
    }
    .main-button > div > button {
        background-color: #0F172A !important;
        color: white !important;
        width: 100%;
        border: none !important;
        height: 64px !important;
        font-size: 18px !important;
    }
    .main-button > div > button:hover {
        background-color: #10B981 !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
    }
    
    /* Health Indicator */
    .health-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
        width: 100%;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .health-online { background-color: rgba(16, 185, 129, 0.1); color: #34D399; }
    .health-offline { background-color: rgba(239, 68, 68, 0.1); color: #F87171; }

    /* Role Selector */
    .role-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 24px 0; }
    .role-item {
        border: 2px solid #E5E7EB;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        background: white;
    }
    .role-item.active {
        border-color: #4FBFA5;
        background-color: #F0FDF4;
    }
    .role-icon { font-size: 24px; margin-bottom: 8px; }
    .role-name { font-weight: 700; font-size: 14px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'Login' 
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = 'mitra'
if 'curr_page' not in st.session_state:
    st.session_state.curr_page = 'Dashboard'

# --- 4. MICROSERVICE CONFIG ---
BASE_URLS = {
    "auth": "http://127.0.0.1:5001",
    "booking": "http://127.0.0.1:5002",
    "inventory": "http://127.0.0.1:5003",
    "payment": "http://127.0.0.1:5004"
}

def call_service(service, endpoint, method="GET", payload=None):
    try:
        url = f"{BASE_URLS[service]}{endpoint}"
        if method == "POST":
            return requests.post(url, json=payload, timeout=2)
        return requests.get(url, timeout=2)
    except:
        return None

# --- 5. AUTHENTICATION PAGES ---
if not st.session_state.authenticated:
    
    # Custom Full-Screen Split Layout
    c_form, c_banner = st.columns([1, 1])
    
    with c_form:
        st.markdown('<div class="auth-form-container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="brand-header">
                <div class="brand-logo">K</div>
                <div class="brand-name">KeepIn <span style="color:#94A3B8; font-weight:500; font-size:16px;">Console</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.auth_page == 'Login':
            st.markdown("<h1 style='font-size:42px !important; margin-bottom:12px;'>Selamat Datang Kembali 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#64748B; font-size:18px; margin-bottom: 3rem;'>Monitor dan kelola ekosistem loker Anda dalam satu dashboard terintegrasi.</p>", unsafe_allow_html=True)
            
            # Role Selection UI
            st.markdown("<p style='font-weight:800; font-size:12px; color:#1F2937; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:16px;'>Identitas Anda</p>", unsafe_allow_html=True)
            roles = [("Mitra", "🟢", "mitra"), ("Penyewa", "🎒", "penyewa"), ("Admin", "🛡️", "admin")]
            
            role_cols = st.columns(3)
            for i, (name, icon, val) in enumerate(roles):
                is_active = st.session_state.selected_role == val
                with role_cols[i]:
                    if st.button(f"{icon} {name}", key=f"role_{val}", use_container_width=True):
                        st.session_state.selected_role = val
                        st.rerun()
            
            st.write("\n")
            email = st.text_input("EMAIL", placeholder="username@corporate.com")
            password = st.text_input("KATA SANDI", type="password", placeholder="••••••••")
            
            st.write("\n")
            st.markdown('<div class="main-button">', unsafe_allow_html=True)
            if st.button("Masuk Ke Akun", key="btn_login"):
                if email and password:
                    res = call_service("auth", "/login", "POST", {
                        "email": email, "password": password, "role": st.session_state.selected_role
                    })
                    if res and res.status_code == 200:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res.json().get("user", {"nama": "User", "role": st.session_state.selected_role})
                        st.rerun()
                    else:
                        st.error("Kredensial tidak valid atau server offline.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<div style='text-align:center; margin-top:32px;'><p style='color:#64748B; font-weight:500;'>Masalah akses? <a href='#' style='color:#10B981; font-weight:700; text-decoration:none;'>Hubungi Helpdesk</a></p></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_banner:
        # High Resolution Illustration Banner
        st.markdown(f"""
            <div style="background: linear-gradient(165deg, #0F172A 0%, #1E293B 100%); height: 100vh; padding: 10vh 8vw; color: white; display:flex; flex-direction:column; justify-content:center; border-left: 1px solid rgba(255,255,255,0.05);">
                <div style="background-color: rgba(16, 185, 129, 0.1); color: #10B981; padding: 6px 14px; border-radius: 8px; font-weight: 800; font-size: 13px; letter-spacing: 0.1em; display: inline-block; width: fit-content; margin-bottom: 32px;">KEEPIN IOT SOLUTIONS</div>
                <h1 style="color:white; font-size:64px !important; line-height:1; margin-bottom:24px;">Revolusi <br><span style="color:#10B981;">Logistik</span> Mikro.</h1>
                <p style="color:#94A3B8; font-size:20px; line-height:1.7; margin-bottom:48px; max-width: 500px;">Platform manajemen penitipan barang pintar yang menghubungkan perangkat IoT dengan sistem pembayaran dan inventori secara real-time.</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                    <div style="background: rgba(255,255,255,0.03); padding: 24px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 32px; margin-bottom: 8px;">📊</div>
                        <div style="font-weight:800; font-size:18px; color:white; margin-bottom:4px;">Smart Inventory</div>
                        <p style="color:#64748B; font-size:14px; margin:0;">Pantau ketersediaan unit di ribuan cabang secara instan.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 24px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 32px; margin-bottom: 8px;">🔐</div>
                        <div style="font-weight:800; font-size:18px; color:white; margin-bottom:4px;">IoT Encryption</div>
                        <p style="color:#64748B; font-size:14px; margin:0;">Teknologi enkripsi mutakhir untuk keamanan akses loker fisik.</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. DASHBOARD (AUTHENTICATED) ---
else:
    # Sidebar Setup
    with st.sidebar:
        st.markdown("""
            <div style='margin-bottom:2rem;'>
                <div style="background-color: #4FBFA5; color: white; width: 32px; height: 32px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; margin-right: 8px;">K</div>
                <span style='font-weight:800; font-size:20px; color:white;'>KeepIn</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; margin-bottom: 24px;'>
                <p style='color:#94A3B8; font-size:11px; font-weight:700; letter-spacing:0.05em; margin-bottom:4px; text-transform:uppercase;'>Verified Account</p>
                <p style='font-weight:700; margin:0;'>{st.session_state.user_info['nama']}</p>
                <p style='color:#6FD3B1; font-size:12px; margin:0;'>Role: {st.session_state.user_info['role'].capitalize()}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        pages = ["Dashboard", "Inventori Loker", "Laporan Transaksi", "Pendaftaran Unit"]
        for p in pages:
            if st.button(p, use_container_width=True, type="primary" if st.session_state.curr_page == p else "secondary"):
                st.session_state.curr_page = p
                st.rerun()
        
        st.write("\n" * 5)
        
        # Health Checks
        st.markdown("<p style='color:#6B7280; font-size:11px; font-weight:800; margin-bottom:12px; text-transform:uppercase;'>Service Status</p>", unsafe_allow_html=True)
        services = ["Auth", "Booking", "Inventory", "Payment"]
        for s in services:
            res = call_service(s.lower(), "/health" if s != "Inventory" else "/loker-all")
            status = "Online" if res else "Offline"
            cls = "health-online" if status == "Online" else "health-offline"
            st.markdown(f'<div class="health-badge {cls}">● {s}: {status}</div>', unsafe_allow_html=True)
        
        st.write("\n")
        if st.button("Keluar Sistem", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- MAIN CONTENT ---
    # Container with padding for non-auth pages
    st.markdown('<div style="padding: 3rem 5vw;">', unsafe_allow_html=True)
    
    if st.session_state.curr_page == "Dashboard":
        row_h = st.columns([2, 1])
        with row_h[0]:
            st.markdown(f"<h1 style='font-size:48px !important; margin-bottom:8px;'>Dashboard Utama</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#64748B; font-size:20px;'>Selamat datang kembali, <b>{st.session_state.user_info['nama']}</b>.</p>", unsafe_allow_html=True)
        with row_h[1]:
            st.markdown("<div style='text-align:right;'><div style='background:#F1F5F9; padding:12px 24px; border-radius:12px; display:inline-block;'><p style='color:#94A3B8; font-weight:800; font-size:11px; margin:0; text-transform:uppercase;'>LOKASI DATA</p><h4 style='margin:0; font-weight:800; color:#0F172A;'>Cloud Cluster Jakarta</h4></div></div>", unsafe_allow_html=True)

        st.write("\n" * 2)
        
        # Logic to fetch real data
        res_i = call_service("inventory", "/loker-all")
        res_b = call_service("booking", "/booking")
        
        inv_data = res_i.json() if res_i else []
        total_loker = len(inv_data)
        available = len([l for l in inv_data if l.get('status_loker') == 'Tersedia'])
        total_bookings = len(res_b.json()) if res_b else 0
        
        # Stats Grid
        m_cols = st.columns(4)
        stats = [
            ("TOTAL PENDAPATAN", "Rp 4.2M", "↑ 12%", "delta-up"),
            ("UNIT LOKER", str(total_loker), "Active", "delta-up"),
            ("READY TO BOOK", str(available), "Units", "delta-up"),
            ("HITS TRANSAKSI", str(total_bookings), "Lifetime", "delta-up")
        ]
        
        for i, (label, val, delta, d_cls) in enumerate(stats):
            with m_cols[i]:
                st.markdown(f"""
                    <div class="bento-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{val}</div>
                        <div class="metric-delta {d_cls}">{delta}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.write("\n")
        
        # Table Section
        st.markdown("<h3 style='margin-bottom:24px;'>Aktivitas Unit Terkini</h3>", unsafe_allow_html=True)
        if inv_data:
            df = pd.DataFrame(inv_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown("""
                <div style="background:#F8FAFC; padding:60px; border-radius:24px; text-align:center; border: 2px dashed #E2E8F0;">
                    <p style="color:#94A3B8; font-weight:700; font-size:18px;">Menghubungkan ke Inventory microservice...</p>
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.curr_page == "Laporan Transaksi":
        st.markdown("<h1>Laporan Keuangan 📊</h1>", unsafe_allow_html=True)
        res_p = call_service("payment", "/payment")
        if res_p and res_p.status_code == 200:
            st.dataframe(pd.DataFrame(res_p.json()), use_container_width=True)
        else:
            st.error("Gagal menarik data dari Payment Service.")

    elif st.session_state.curr_page == "Inventori Loker":
        st.markdown("<h1>Manajemen Aset Loker 📦</h1>", unsafe_allow_html=True)
        st.write("Fitur ini memungkinkan Anda memantau status IoT setiap loker secara remote.")
        res_i = call_service("inventory", "/loker-all")
        if res_i:
            st.dataframe(pd.DataFrame(res_i.json()), use_container_width=True)
        else:
            st.warning("Inventory Service sedang tidak merespon.")

    else:
        st.info("Halaman ini sedang dalam pengembangan.")
    st.markdown('</div>', unsafe_allow_html=True)