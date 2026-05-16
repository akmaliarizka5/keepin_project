import streamlit as st
import pandas as pd
import requests
import datetime

# --- 1. SET CONFIG ---
st.set_page_config(
    page_title="KeepIn Partner Console",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS FOR MAJESTIC & BOLD BRANDING (Matching React Preview) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset & Base */
    .block-container { padding: 2rem 4rem !important; max-width: 1200px; margin: 0 auto; }
    [data-testid="stSidebar"] { background-color: #1F2937 !important; color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* Typography */
    h1, h2, h3, .brand-font {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
    }
    
    p, span, label, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
    }

    /* Custom Header Branding */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2rem;
    }
    .brand-logo {
        background-color: #4FBFA5;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 20px;
    }
    .brand-name {
        font-weight: 800;
        font-size: 24px;
        color: #1F2937;
    }

    /* Bento Cards */
    .bento-card {
        background: white;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .bento-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #4FBFA5;
    }
    
    .metric-label {
        font-size: 13px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 4px;
    }
    .metric-delta {
        font-size: 14px;
        font-weight: 600;
    }
    .delta-up { color: #10B981; }
    .delta-down { color: #EF4444; }

    /* Forms & Inputs */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
    }
    .main-button > div > button {
        background-color: #1F2937 !important;
        color: white !important;
        width: 100%;
        border: none !important;
    }
    .main-button > div > button:hover {
        background-color: #4FBFA5 !important;
        transform: scale(1.02);
    }
    
    /* Sidebar Navigation Fixes */
    .st-emotion-cache-1ecpynv { background-color: #374151 !important; margin: 4px 0; border-radius: 8px !important; }
    .st-emotion-cache-1ecpynv:hover { background-color: #4FBFA5 !important; }

    /* Health Indicator */
    .health-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
        width: 100%;
    }
    .health-online { background-color: #D1FAE5; color: #065F46; }
    .health-offline { background-color: #FEE2E2; color: #991B1B; }

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
    
    # Simple Layout for Auth
    c1, spacer, c2 = st.columns([1.2, 0.2, 1.3])
    
    with c1:
        st.markdown("""
            <div style="padding-top: 4rem;">
                <div class="brand-header">
                    <div class="brand-logo">K</div>
                    <div class="brand-name">KeepIn <span style="color:#94A3B8; font-weight:500; font-size:16px;">Partner</span></div>
                </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.auth_page == 'Login':
            st.markdown("<h1>Selamat Datang Kembali 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#64748B; margin-bottom: 2rem;'>Masuk untuk mengelola loker dan memantau bisnis Anda.</p>", unsafe_allow_html=True)
            
            # Role Selection UI
            st.markdown("<p style='font-weight:700; font-size:12px; color:#94A3B8; text-transform:uppercase;'>Pilih Peran</p>", unsafe_allow_html=True)
            roles = [("Mitra", "🟢", "mitra"), ("Penyewa", "🎒", "penyewa"), ("Admin", "🛡️", "admin")]
            
            cols = st.columns(3)
            for i, (name, icon, val) in enumerate(roles):
                is_active = st.session_state.selected_role == val
                with cols[i]:
                    if st.button(f"{icon}\n{name}", key=f"role_{val}", use_container_width=True, 
                                 type="secondary" if not is_active else "primary"):
                        st.session_state.selected_role = val
                        st.rerun()
            
            st.write("\n")
            email = st.text_input("EMAIL", placeholder="your@email.com")
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
            
            st.markdown("<div style='text-align:center; margin-top:20px;'><p style='color:#64748B;'>Belum punya akun? <a href='#' style='color:#4FBFA5; font-weight:700;'>Hubungi Admin</a></p></div>", unsafe_allow_html=True)

    with c2:
        # Illustration / Banner Area
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1F2937 0%, #111827 100%); height: 85vh; border-radius: 40px; padding: 60px; color: white; display:flex; flex-direction:column; justify-content:center;">
                <h1 style="color:white; font-size:48px !important; margin-bottom:24px;">Digitalkan Penitipan Barang <span style="color:#6FD3B1;">Sekarang.</span></h1>
                <p style="color:#94A3B8; font-size:18px; line-height:1.6; margin-bottom:40px;">Platform manajemen loker pintar berbasis IoT pertama di Indonesia. Aman, Cepat, dan Terpercaya.</p>
                <div style="background: rgba(255,255,255,0.05); padding: 24px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color:#6FD3B1; font-weight:800; font-size:14px; margin-bottom:4px;">PROMO MITRA BARU</div>
                    <div style="font-weight:700; font-size:18px;">Komisi 0% untuk 3 bulan pertama.</div>
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
    if st.session_state.curr_page == "Dashboard":
        row1 = st.columns([2, 1])
        with row1[0]:
            st.markdown(f"<h1>Hai, {st.session_state.user_info['nama']}! 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#64748B; font-size:18px;'>Berikut adalah ringkasan performa unit loker Anda hari ini.</p>", unsafe_allow_html=True)
        with row1[1]:
            st.markdown("<div style='text-align:right;'><p style='color:#94A3B8; font-weight:700; font-size:14px;'>PERIODE</p><h3 style='margin-top:-5px;'>Mei 2026</h3></div>", unsafe_allow_html=True)

        st.write("\n")
        
        # Stats Grid
        res_i = call_service("inventory", "/loker-all")
        res_b = call_service("booking", "/booking")
        
        total_loker = len(res_i.json()) if res_i else 12
        available = len([l for l in res_i.json() if l.get('status_loker') == 'Tersedia']) if res_i else 8
        total_bookings = len(res_b.json()) if res_b else 156
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
                <div class="bento-card">
                    <div class="metric-label">Pendapatan (IDR)</div>
                    <div class="metric-value">4.2M</div>
                    <div class="metric-delta delta-up">↑ 12% vs bln lalu</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="bento-card">
                    <div class="metric-label">Unit Loker</div>
                    <div class="metric-value">{total_loker}</div>
                    <div class="metric-delta" style="color:#94A3B8;">Total Kapasitas</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="bento-card">
                    <div class="metric-label">Tersedia</div>
                    <div class="metric-value" style="color:#10B981;">{available}</div>
                    <div class="metric-delta delta-up">Ready to use</div>
                </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
                <div class="bento-card">
                    <div class="metric-label">Transaksi</div>
                    <div class="metric-value">{total_bookings}</div>
                    <div class="metric-delta delta-up">↑ 48 hari ini</div>
                </div>
            """, unsafe_allow_html=True)

        st.write("\n")
        
        # Table Section
        st.markdown("<h3>Unit Cabang Teraktif</h3>", unsafe_allow_html=True)
        if res_i and res_i.status_code == 200:
            df = pd.DataFrame(res_i.json())
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Menunggu data dari Inventory Microservice...")

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