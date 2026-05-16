import streamlit as st
import pandas as pd
import requests

# --- 1. SET CONFIG & ANTI-STREAMLIT PADDING BUSTER ---
st.set_page_config(page_title="KeepIn Console", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS untuk merombak tampilan agar presisi dan elegan di browser
st.markdown("""
    <style>
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .stApp { background-color: #FFFFFF; }
    
    label[data-testid="stWidgetLabel"] {
        color: #4A5568 !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    
    div.btn-utama > div > button {
        background-color: #1A202C !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 14px 24px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100% !important;
    }
    
    .role-card-active {
        border: 2px solid #4FD1C5;
        background-color: #F0FDF4;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .role-card-inactive {
        border: 1px solid #E2E8F0;
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        border: 1px solid #EDF2F7;
    }
    .status-box {
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-size: 13px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'Login' 
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = 'mitra'
if 'dashboard_page' not in st.session_state:
    st.session_state.dashboard_page = 'Beranda'

# URL Gerbang Akses Microservices Lokal
BASE_URLS = {
    "auth": "http://127.0.0.1:5001",
    "booking": "http://127.0.0.1:5002",
    "inventory": "http://127.0.0.1:5003",
    "payment": "http://127.0.0.1:5004"
}

def fetch_data_from_service(service_name, endpoint, method="GET", json_data=None):
    try:
        url = f"{BASE_URLS[service_name]}{endpoint}"
        if method == "POST":
            return requests.post(url, json=json_data, timeout=3)
        return requests.get(url, timeout=3)
    except Exception:
        return None

# ==============================================================================
# JALUR 1: SISTEM LOG IN & DAFTAR (SPLIT SCREEN BROWSER)
# ==============================================================================
if not st.session_state.authenticated:
    
    if st.session_state.auth_page == 'Login':
        col_form, col_banner = st.columns([1, 1])
        with col_form:
            st.markdown('<div style="padding: 50px 12% 20px 12%;">', unsafe_allow_html=True)
            st.markdown('### 🟢 KeepIn <span style="background-color:#E6FFFA; color:#4FD1C5; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:bold;">Mitra</span>', unsafe_allow_html=True)
            st.write("\n")
            st.markdown('<h1 style="font-size: 32px; font-weight:800; color:#1A202C; margin-bottom:5px;">Selamat datang kembali! 👋</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px; margin-bottom:30px;">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</p>', unsafe_allow_html=True)
            
            st.markdown('<p style="font-size:11px; font-weight:700; color:#4A5568; margin-bottom:10px;">PILIH ROLE ANDA</p>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1:
                is_active = st.session_state.selected_role == 'mitra'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}">🟢<br><b>Mitra</b><br><span style="font-size:10px; color:#A0AEC0;">Kelola loker</span></div>', unsafe_allow_html=True)
                if st.button("Set Mitra", key="set_r_mitra", use_container_width=True):
                    st.session_state.selected_role = 'mitra'
                    st.rerun()
            with r2:
                is_active = st.session_state.selected_role == 'penyewa'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}">🎒<br><b>Penyewa</b><br><span style="font-size:10px; color:#A0AEC0;">Booking mudah</span></div>', unsafe_allow_html=True)
                if st.button("Set Penyewa", key="set_r_penyewa", use_container_width=True):
                    st.session_state.selected_role = 'penyewa'
                    st.rerun()
            with r3:
                is_active = st.session_state.selected_role == 'admin'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}">🛡️<br><b>Admin</b><br><span style="font-size:10px; color:#A0AEC0;">Sistem</span></div>', unsafe_allow_html=True)
                if st.button("Set Admin", key="set_r_admin", use_container_width=True):
                    st.session_state.selected_role = 'admin'
                    st.rerun()
            
            st.write("\n")
            email = st.text_input("EMAIL", placeholder="Masukkan email Anda")
            password = st.text_input("KATA SANDI", type="password", placeholder="Masukkan kata sandi")
            st.checkbox("Ingat saya", key="chk_remember")
            
            st.write("\n")
            st.markdown('<div class="btn-utama">', unsafe_allow_html=True)
            if st.button("Masuk ke Akun", key="action_login"):
                if email and password:
                    res = fetch_data_from_service("auth", "/login", "POST", {"email": email, "password": password, "role": st.session_state.selected_role})
                    if res and res.status_code == 200:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res.json()["user"]
                        st.rerun()
                    else:
                        st.error("Gagal Masuk: Akun tidak ditemukan atau role tidak sesuai.")
                else:
                    st.warning("Kolom email & sandi wajib diisi.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("\n")
            st.markdown('<p style="text-align:center; font-size:13px; color:#718096; margin-bottom: 0;">Belum punya akun mitra?</p>', unsafe_allow_html=True)
            if st.button("Daftar Kemitraan Baru ↗", key="go_to_reg", use_container_width=True):
                st.session_state.auth_page = 'SignUp'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_banner:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #F0FDF4 0%, #E6FFFA 100%); height: 100vh; padding: 90px 12% 40px 12%; border-left: 1px solid #EDF2F7;">
                    <h1 style="font-size: 38px; font-weight: 800; color: #1A202C; line-height: 1.25; margin-bottom:20px;">
                        Satu platform untuk <br><span style="color: #4FD1C5;">semua kebutuhan</span> loker.
                    </h1>
                    <p style="color: #4A5568; font-size: 15px; margin-bottom: 45px; line-height:1.6;">
                        Baik Anda mitra pemilik properti, penyewa yang sedang bepergian, atau admin platform. KeepIn siap mendigitalkan penitipan barang Anda.
                    </p>
                    <div style="margin-bottom: 25px;">
                        <h5 style="margin:0 0 4px 0; color:#2D3748; font-size:15px;">🟢 Kelola Bisnis Lebih Mudah</h5>
                        <p style="margin:0; color:#718096; font-size:13px;">Pantau pendapatan, kuota booking, dan performa IoT loker secara real-time.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.auth_page == 'SignUp':
        col_dark, col_reg_form = st.columns([1, 1])
        with col_dark:
            st.markdown("""
                <div style="background-color: #1A202C; color: white; height: 100vh; padding: 100px 12% 40px 12%; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h3 style="color:#4FD1C5; margin-bottom:40px;">🟢 KeepIn Console</h3>
                        <h1 style="font-size: 38px; font-weight: 800; line-height: 1.3; margin-bottom:20px;">Mulai kelola loker Anda dengan profesional.</h1>
                    </div>
                    <div>
                        <p style="color:#718096; font-size:11px; margin:0;">PLATFORM STATUS</p>
                        <p style="color:#48BB78; font-size:12px; font-weight:bold; margin:0;">● Sistem Berjalan - Production Mode</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_reg_form:
            st.markdown('<div style="padding: 50px 15% 40px 12%;">', unsafe_allow_html=True)
            if st.button("← KEMBALI KE LOGIN", key="back_to_login"):
                st.session_state.auth_page = 'Login'
                st.rerun()
                
            st.markdown('<h1 style="font-size: 32px; font-weight:800; color:#1A202C; margin-top:20px; margin-bottom:5px;">Daftar Akun Baru</h1>', unsafe_allow_html=True)
            
            reg_nama = st.text_input("NAMA LENGKAP", placeholder="Contoh: Andi Pratama")
            reg_email = st.text_input("EMAIL", placeholder="nama@email.com")
            reg_hp = st.text_input("NOMOR HANDPHONE", placeholder="081234567xxx")
            reg_pass = st.text_input("KATA SANDI", type="password", placeholder="Minimal 8 karakter")
            
            st.write("\n")
            st.markdown('<div class="btn-utama">', unsafe_allow_html=True)
            if st.button("Daftar Akun", key="do_register"):
                if reg_nama and reg_email and reg_pass:
                    payload = {"nama": reg_nama, "email": reg_email, "password": reg_pass, "no_hp": reg_hp, "role": "mitra"}
                    res = fetch_data_from_service("auth", "/register", "POST", payload)
                    if res and res.status_code == 201:
                        st.success("Registrasi Sukses! Silakan Login.")
                        st.session_state.auth_page = 'Login'
                        st.rerun()
                    else:
                        st.error("Gagal mendaftar. Email mungkin telah digunakan.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# JALUR 2: CORE MONITORING WORKSPACE (REAL-TIME DATA DARI MICROSERVICES)
# ==============================================================================
else:
    # 1. Tarik Data Real-time Asli dari Seluruh Microservices Backend
    res_b = fetch_data_from_service("booking", "/booking")
    res_p = fetch_data_from_service("payment", "/payment")
    res_i = fetch_data_from_service("inventory", "/loker-all") # Mengambil seluruh data loker/usaha mitra
    
    # Deteksi Status Koneksi Keinginan
    b_status = "Online" if res_b else "Offline"
    p_status = "Online" if res_p else "Offline"
    i_status = "Online" if res_i else "Offline"
    
    # Parsing ke Dataframe Pandas untuk agregasi visual komponen
    df_booking = pd.DataFrame(res_b.json()) if res_b and res_b.status_code == 200 else pd.DataFrame()
    df_payment = pd.DataFrame(res_p.json()) if res_p and res_p.status_code == 200 else pd.DataFrame()
    df_inventory = pd.DataFrame(res_i.json()) if res_i and res_i.status_code == 200 else pd.DataFrame()

    # Panel Sidebar Navigasi & Status Layanan
    with st.sidebar:
        st.markdown(f'### 🏢 KeepIn <span style="font-size:10px; background:#4FD1C5; color:white; padding:2px 6px; border-radius:4px;">{st.session_state.user_info["role"].upper()}</span>', unsafe_allow_html=True)
        st.write(f"Mitra: **{st.session_state.user_info['nama']}**")
        st.markdown("---")
        
        st.button("🏠 Beranda", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Beranda"}))
        st.button("📋 Pendaftaran Usaha", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Pendaftaran"}))
        st.button("📊 Laporan Bisnis", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Laporan"}))
        st.markdown("---")
        
        st.write("**SYSTEM HEALTH MONITOR**")
        for s_title, s_stat in [("Auth Service", "Online"), ("Booking Service", b_status), ("Inventory Service", i_status), ("Payment Service", p_status)]:
            bg_box = "#DEF7EC" if s_stat == "Online" else "#FDE8E8"
            tx_box = "#03543F" if s_stat == "Online" else "#9B1C1C"
            st.markdown(f'<div class="status-box" style="background-color: {bg_box}; color: {tx_box};">● {s_title}: {s_stat}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("⬅️ Keluar", use_container_width=True, key="btn_logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    # Konten Utama Dashboard Konsol
    st.markdown('<div style="padding: 30px 40px;">', unsafe_allow_html=True)
    
    if st.session_state.dashboard_page == 'Beranda':
        t_left, t_right = st.columns([3, 1])
        with t_left:
            st.markdown(f'<h1 style="font-size:26px; font-weight:800; color:#1A202C; margin:0;">Selamat datang kembali, {st.session_state.user_info["nama"]}! 👋</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px;">Data di bawah ditarik langsung secara live dari ekosistem Microservices.</p>', unsafe_allow_html=True)
        with t_right:
            st.selectbox("FILTER CABANG", ["Semua Cabang Terdaftar"], label_visibility="collapsed")

        st.write("\n")
        # Banner Statis Daftarkan Usaha Baru
        st.markdown("""
            <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #4FD1C5; background: white;">
                <div>
                    <h4 style="margin: 0; color: #2D3748; font-size:15px;">Daftarkan Cabang Loker Baru</h4>
                    <p style="font-size: 13px; color: #718096; margin: 0;">Tambahkan titik usaha baru Anda untuk memperluas cakupan wilayah sewa IoT KeepIn.</p>
                </div>
                <div style="background-color: #1A202C; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700; font-size: 12px;">
                    BUAT PERMOHONAN
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("\n")
        
        # --- HITUNG METRIK LIVE DARI HASIL AGREGASI DATAFRAME DATABASE ---
        if not df_inventory.empty:
            total_cabang = df_inventory['nama_cabang'].nunique() if 'nama_cabang' in df_inventory.columns else 0
            total_loker = len(df_inventory)
            loker_aktif = len(df_inventory[df_inventory['status_loker'].str.lower() == 'tersedia']) if 'status_loker' in df_inventory.columns else 0
        else:
            total_cabang, total_loker, loker_aktif = 0, 0, 0

        total_b = len(df_booking) if not df_booking.empty else 0

        # Menampilkan Grid Metrik Riil Komputerisasi Backend
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL USAHA</p><h2 style="margin:5px 0;">{total_cabang}</h2><p style="color:#48BB78; font-size:11px; margin:0;">● Terkoneksi DB</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL LOKER FISIK</p><h2 style="margin:5px 0;">{total_loker}</h2><p style="color:#48BB78; font-size:11px; margin:0;">● Terdaftar Sistem</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">LOKER SIAP PAKAI</p><h2 style="margin:5px 0;">{loker_aktif}</h2><p style="color:#48BB78; font-size:11px; margin:0;">🟢 Status: Kosong</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL TRANSAKSI BOOKING</p><h2 style="margin:5px 0;">{total_b}</h2><p style="color:#48BB78; font-size:11px; margin:0;">📊 Riwayat Aktivitas</p></div>', unsafe_allow_html=True)

        st.write("\n\n")
        st.markdown('<p style="font-size:12px; font-weight:700; color:#718096; letter-spacing:0.5px;">STRUKTUR CABANG AKTIF (DATA INVENTORY SERVICE)</p>', unsafe_allow_html=True)
        
        # MENAMPILKAN TABEL DATABASE ASLI
        if not df_inventory.empty:
            # Mengelompokkan data per cabang secara agregat agar rapi dibaca di tabel dashboard
            tabel_cabang = df_inventory.groupby('nama_cabang').agg(
                ALAMAT_OPERASIONAL=('alamat', 'first'),
                KAPASITAS_UNIT_LOKER=('id_loker', 'count')
            ).reset_index()
            
            # Ubah nama kolom agar terlihat profesional seperti mockup UI/UX
            tabel_cabang.columns = ["NAMA UNIT CABANG", "ALAMAT OPERASIONAL BISNIS", "TOTAL UNIT KAPASITAS LOKER"]
            st.dataframe(tabel_cabang, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Belum ada data cabang usaha yang terdeteksi di database `inventory_db`.")

    elif st.session_state.dashboard_page == 'Laporan':
        st.markdown('<h1 style="font-size:28px; font-weight:800;">Laporan Performa Bisnis 📊</h1>', unsafe_allow_html=True)
        if not df_payment.empty:
            st.write("### LOG TRANSAKSI KEUANGAN ASLI (PAYMENT SERVICE)")
            st.dataframe(df_payment, use_container_width=True, hide_index=True)
        else:
            st.info("Menunggu data transaksi pembayaran masuk dari payment_service.")
            
    st.markdown('</div>', unsafe_allow_html=True)