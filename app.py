import streamlit as st
import pandas as pd
import requests

# --- 1. SET CONFIG & BIG FONT OVERRIDE ---
st.set_page_config(page_title="KeepIn Console", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS Skala Besar untuk memastikan seluruh teks dan form berukuran besar dan jelas
st.markdown("""
    <style>
    /* Reset & Container Base full screen */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .stApp { background-color: #FAFBFC; }
    
    /* 🔴 PAKSA UKURAN FONT GLOBAL RAKSASA */
    html, body, [data-testid="stMarkdownContainer"] p, .stMarkdown, p, span {
        font-size: 18px !important; /* Standar teks paragraf diperbesar tajam */
        line-height: 1.7 !important;
        color: #2D3748 !important;
    }
    
    /* Memperbesar Judul Halaman Utama */
    h1 { font-size: 46px !important; font-weight: 800 !important; color: #1A202C !important; }
    h2 { font-size: 36px !important; font-weight: 800 !important; color: #1A202C !important; }
    h3 { font-size: 26px !important; font-weight: 700 !important; color: #1A202C !important; }
    h4 { font-size: 22px !important; font-weight: 700 !important; color: #1A202C !important; }
    
    /* Memperbesar Label Form Input (EMAIL, KATA SANDI, dll) */
    label[data-testid="stWidgetLabel"] p {
        color: #1A202C !important;
        font-weight: 800 !important;
        font-size: 15px !important; /* Label dipertebal dan diperbesar */
        letter-spacing: 1px;
        margin-bottom: 10px !important;
    }
    
    /* Memperbesar Kolom Ketik / Box Input Text */
    div[data-testid="stTextInput"] input {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        border: 2px solid #CBD5E0 !important; /* Border dipertebal */
        border-radius: 14px !important;
        padding: 16px 20px !important; /* Padding dalam diperlebar */
        font-size: 18px !important; /* Teks ketikan diperbesar */
        height: auto !important;
    }
    
    /* Memperbesar Tombol Utama Hitam */
    div.btn-utama > div > button {
        background-color: #1A202C !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 18px 32px !important; /* Tombol jadi lebih tinggi dan gagah */
        font-weight: 800 !important;
        font-size: 20px !important; /* Teks tombol diperbesar */
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Memperbesar Kartu Seleksi Peran (Role Cards) */
    .role-card-active {
        border: 3px solid #4FD1C5;
        background-color: #F0FDF4;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(79, 209, 197, 0.12);
    }
    .role-card-inactive {
        border: 2px solid #E2E8F0;
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    
    /* Memperbesar Kartu Metrik Angka di Dashboard */
    .metric-card {
        background-color: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.02);
        border: 2px solid #E2E8F0;
    }
    
    /* Memperbesar Teks Status Kesehatan System di Sidebar */
    .status-box {
        padding: 14px 18px;
        border-radius: 14px;
        margin-bottom: 12px;
        font-size: 16px;
        font-weight: 700;
    }
    
    /* Memperbesar Ukuran Checkbox bawaan Streamlit */
    div[data-testid="stCheckbox"] label span {
        font-size: 17px !important;
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
# JALUR 1: SISTEM LOG IN & DAFTAR (MAJESTIC & BOLD VIEW)
# ==============================================================================
if not st.session_state.authenticated:
    
    if st.session_state.auth_page == 'Login':
        col_form, col_banner = st.columns([1.1, 0.9])
        with col_form:
            # Padding diperlebar agar letak komponen tetap simetris di tengah screen
            st.markdown('<div style="padding: 70px 90px 40px 110px;">', unsafe_allow_html=True)
            st.markdown('<h2>🟢 KeepIn <span style="background-color:#E6FFFA; color:#4FD1C5; font-size:15px; padding:4px 12px; border-radius:6px; font-weight:bold;">Mitra</span></h2>', unsafe_allow_html=True)
            st.write("\n")
            st.markdown('<h1>Selamat datang kembali! 👋</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:17px; margin-bottom:40px;">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</p>', unsafe_allow_html=True)
            
            st.markdown('<p style="font-size:15px; font-weight:800; color:#1A202C; margin-bottom:15px; letter-spacing:0.5px;">PILIH ROLE ANDA</p>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1:
                is_active = st.session_state.selected_role == 'mitra'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}"><span style="font-size:28px;">🟢</span><br><b style="font-size:18px;">Mitra</b><br><span style="font-size:14px; color:#718096;">Kelola loker</span></div>', unsafe_allow_html=True)
                if st.button("Set Mitra", key="set_r_mitra", use_container_width=True):
                    st.session_state.selected_role = 'mitra'
                    st.rerun()
            with r2:
                is_active = st.session_state.selected_role == 'penyewa'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}"><span style="font-size:28px;">🎒</span><br><b style="font-size:18px;">Penyewa</b><br><span style="font-size:14px; color:#718096;">Booking mudah</span></div>', unsafe_allow_html=True)
                if st.button("Set Penyewa", key="set_r_penyewa", use_container_width=True):
                    st.session_state.selected_role = 'penyewa'
                    st.rerun()
            with r3:
                is_active = st.session_state.selected_role == 'admin'
                st.markdown(f'<div class="{"role-card-active" if is_active else "role-card-inactive"}"><span style="font-size:28px;">🛡️</span><br><b style="font-size:18px;">Admin</b><br><span style="font-size:14px; color:#718096;">Sistem</span></div>', unsafe_allow_html=True)
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
            st.markdown('<p style="text-align:center; font-size:16px; color:#718096; margin-bottom: 8px;">Belum punya akun mitra?</p>', unsafe_allow_html=True)
            if st.button("Daftar Kemitraan Baru ↗", key="go_to_reg", use_container_width=True):
                st.session_state.auth_page = 'SignUp'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_banner:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #F0FDF4 0%, #E6FFFA 100%); height: 100vh; padding: 130px 90px 40px 90px; border-left: 2px solid #E2E8F0;">
                    <h1 style="font-size: 48px !important; font-weight: 800; line-height: 1.35; margin-bottom:28px;">
                        Satu platform untuk <br><span style="color: #4FD1C5;">semua kebutuhan</span> loker.
                    </h1>
                    <p style="color: #4A5568; font-size: 18px !important; margin-bottom: 50px; line-height:1.7;">
                        Baik Anda mitra pemilik properti, penyewa yang sedang bepergian, atau admin platform. KeepIn siap mendigitalkan penitipan barang Anda dengan mulus.
                    </p>
                    <div style="margin-bottom: 35px;">
                        <h3 style="margin:0 0 8px 0; color:#2D3748; font-size:22px !important; font-weight:800;">🟢 Kelola Bisnis Lebih Mudah</h3>
                        <p style="margin:0; color:#718096; font-size:15px !important;">Pantau pendapatan, kuota booking, dan performa IoT loker secara real-time.</p>
                    </div>
                    <div style="margin-bottom: 35px;">
                        <h3 style="margin:0 0 8px 0; color:#2D3748; font-size:22px !important; font-weight:800;">🎒 Booking Cepat & Praktis</h3>
                        <p style="margin:0; color:#718096; font-size:15px !important;">Cari loker terdekat yang kosong dan lakukan enkripsi kunci pesanan dalam hitungan detik.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.auth_page == 'SignUp':
        col_dark, col_reg_form = st.columns([0.9, 1.1])
        with col_dark:
            st.markdown("""
                <div style="background-color: #1A202C; color: white; height: 100vh; padding: 130px 90px 40px 90px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h1 style="color:#4FD1C5; margin-bottom:45px; font-weight:800;">🟢 KeepIn Console</h1>
                        <h1 style="font-size: 44px !important; color:white; font-weight: 800; line-height: 1.35; margin-bottom:20px;">Mulai kelola loker Anda dengan profesional.</h1>
                    </div>
                    <div>
                        <p style="color:#A0AEC0; font-size:14px; margin:0; letter-spacing:1px;">PLATFORM STATUS</p>
                        <p style="color:#48BB78; font-size:16px; font-weight:bold; margin:0;">● Sistem Berjalan - Production Mode</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_reg_form:
            st.markdown('<div style="padding: 70px 110px 40px 90px;">', unsafe_allow_html=True)
            if st.button("← KEMBALI KE LOGIN", key="back_to_login"):
                st.session_state.auth_page = 'Login'
                st.rerun()
                
            st.markdown('<h1>Daftar Akun Baru</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:17px; margin-bottom:35px;">Lengkapi data berikut untuk bergabung dengan ekosistem KeepIn.</p>', unsafe_allow_html=True)
            
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
# JALUR 2: CORE MONITORING WORKSPACE (BIG DASHBOARD DESIGN)
# ==============================================================================
else:
    res_b = fetch_data_from_service("booking", "/booking")
    res_p = fetch_data_from_service("payment", "/payment")
    res_i = fetch_data_from_service("inventory", "/loker-all")
    
    b_status = "Online" if res_b else "Offline"
    p_status = "Online" if res_p else "Offline"
    i_status = "Online" if res_i else "Offline"
    
    df_booking = pd.DataFrame(res_b.json()) if res_b and res_b.status_code == 200 else pd.DataFrame()
    df_payment = pd.DataFrame(res_p.json()) if res_p and res_p.status_code == 200 else pd.DataFrame()
    df_inventory = pd.DataFrame(res_i.json()) if res_i and res_i.status_code == 200 else pd.DataFrame()

    with st.sidebar:
        st.markdown(f'<h2 style="font-size:24px !important; font-weight:800; margin-bottom:5px;">🏢 KeepIn <span style="font-size:13px; background:#4FD1C5; color:white; padding:3px 8px; border-radius:6px;">{st.session_state.user_info["role"].upper()}</span></h2>', unsafe_allow_html=True)
        st.markdown(f"Mitra: <b style='font-size:16px;'>{st.session_state.user_info['nama']}</b>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Tombol navigasi sidebar juga ikut dimodifikasi besar melalui CSS global bawaan Streamlit
        st.button("🏠 Beranda", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Beranda"}))
        st.button("📋 Pendaftaran Usaha", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Pendaftaran"}))
        st.button("📊 Laporan Bisnis", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Laporan"}))
        st.markdown("---")
        
        st.markdown("<b style='font-size:14px; color:#A0AEC0;'>SYSTEM HEALTH MONITOR</b>", unsafe_allow_html=True)
        for s_title, s_stat in [("Auth Service", "Online"), ("Booking Service", b_status), ("Inventory Service", i_status), ("Payment Service", p_status)]:
            bg_box = "#DEF7EC" if s_stat == "Online" else "#FDE8E8"
            tx_box = "#03543F" if s_stat == "Online" else "#9B1C1C"
            st.markdown(f'<div class="status-box" style="background-color: {bg_box}; color: {tx_box};">● {s_title}: {s_stat}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("⬅️ Keluar / Logout", use_container_width=True, key="btn_logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    # Konten Utama Dashboard Konsol Luas
    st.markdown('<div style="padding: 50px 60px;">', unsafe_allow_html=True)
    
    if st.session_state.dashboard_page == 'Beranda':
        t_left, t_right = st.columns([3, 1])
        with t_left:
            st.markdown(f'<h1>Selamat datang kembali, {st.session_state.user_info["nama"]}! 👋</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:17px; margin-top:6px;">Data di bawah ditarik langsung secara live dari ekosistem Microservices.</p>', unsafe_allow_html=True)
        with t_right:
            st.selectbox("FILTER CABANG", ["Semua Cabang Terdaftar"], label_visibility="collapsed")

        st.write("\n")
        # Banner Daftarkan Cabang Baru
        st.markdown("""
            <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 6px solid #4FD1C5; background: white; padding:30px 40px;">
                <div>
                    <h2 style="margin: 0 0 6px 0; font-size:22px !important; font-weight:800;">Daftarkan Cabang Loker Baru</h2>
                    <p style="font-size: 15px !important; color: #718096; margin: 0;">Tambahkan titik usaha baru Anda untuk memperluas cakupan wilayah sewa IoT KeepIn.</p>
                </div>
                <div style="background-color: #1A202C; color: white; padding: 14px 28px; border-radius: 12px; font-weight: bold; font-size: 15px; letter-spacing:0.5px; cursor:pointer;">
                    BUAT PERMOHONAN
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("\n")
        
        # Agregasi data riil database
        if not df_inventory.empty:
            total_cabang = df_inventory['nama_cabang'].nunique() if 'nama_cabang' in df_inventory.columns else 0
            total_loker = len(df_inventory)
            loker_aktif = len(df_inventory[df_inventory['status_loker'].str.lower() == 'tersedia']) if 'status_loker' in df_inventory.columns else 0
        else:
            total_cabang, total_loker, loker_aktif = 0, 0, 0

        total_b = len(df_booking) if not df_booking.empty else 0

        # Grid Metrik Utama Dengan Angka Jumbo Ukuran H1 (Sangat Jelas)
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:13px; font-weight:800; margin:0; letter-spacing:0.5px;">TOTAL USAHA</p><h1 style="margin:10px 0; font-size:48px !important; font-weight:800; color:#1A202C;">{total_cabang}</h1><p style="color:#48BB78; font-size:13px; font-weight:600; margin:0;">● Terkoneksi DB</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:13px; font-weight:800; margin:0; letter-spacing:0.5px;">TOTAL LOKER FISIK</p><h1 style="margin:10px 0; font-size:48px !important; font-weight:800; color:#1A202C;">{total_loker}</h1><p style="color:#48BB78; font-size:13px; font-weight:600; margin:0;">● Terdaftar Sistem</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:13px; font-weight:800; margin:0; letter-spacing:0.5px;">LOKER SIAP PAKAI</p><h1 style="margin:10px 0; font-size:48px !important; font-weight:800; color:#1A202C;">{loker_aktif}</h1><p style="color:#48BB78; font-size:13px; font-weight:600; margin:0;">🟢 Status: Kosong</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:13px; font-weight:800; margin:0; letter-spacing:0.5px;">TOTAL TRANSAKSI</p><h1 style="margin:10px 0; font-size:48px !important; font-weight:800; color:#1A202C;">{total_b}</h1><p style="color:#48BB78; font-size:13px; font-weight:600; margin:0;">📊 Riwayat Aktivitas</p></div>', unsafe_allow_html=True)

        st.write("\n\n")
        st.markdown('<p style="font-size:15px; font-weight:800; color:#718096; letter-spacing:0.8px; margin-bottom:15px;">STRUKTUR CABANG AKTIF (DATA INVENTORY SERVICE)</p>', unsafe_allow_html=True)
        
        # Tabel Cabang Utama Terintegrasi
        if not df_inventory.empty:
            tabel_cabang = df_inventory.groupby('nama_cabang').agg(
                ALAMAT_OPERASIONAL=('alamat', 'first'),
                KAPASITAS_UNIT_LOKER=('id_loker', 'count')
            ).reset_index()
            
            tabel_cabang.columns = ["NAMA UNIT CABANG", "ALAMAT OPERASIONAL BISNIS", "TOTAL UNIT KAPASITAS LOKER"]
            st.dataframe(tabel_cabang, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Belum ada data cabang usaha yang terdeteksi di database `inventory_db`.")

    elif st.session_state.dashboard_page == 'Laporan':
        st.markdown('<h1>Laporan Performa Bisnis 📊</h1>', unsafe_allow_html=True)
        if not df_payment.empty:
            st.write("### LOG TRANSAKSI KEUANGAN RETAIL (PAYMENT SERVICE)")
            st.dataframe(df_payment, use_container_width=True, hide_index=True)
        else:
            st.info("Menunggu masuknya rekaman log data transaksi keuangan dari payment_service.")
            
    st.markdown('</div>', unsafe_allow_html=True)