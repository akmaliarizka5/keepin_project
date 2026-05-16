import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. INISIALISASI SESSION STATE UNTUK AUTENTIKASI ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'Login'  # Pilihan: 'Login' atau 'SignUp'
if 'dashboard_page' not in st.session_state:
    st.session_state.dashboard_page = 'Beranda'

# Konfigurasi Dasar Tampilan
st.set_page_config(page_title="KeepIn - Platform Solusi Loker", layout="wide")

# Konfigurasi Gaya CSS agar Menyerupai Mockup UI/UX Bisnis Tingkat Tinggi
st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp { background-color: #FAFAFA; }
    
    /* Input Customization */
    div.stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        padding: 12px;
    }
    
    /* Card Elements styling */
    .metric-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        border: 1px solid #EDF2F7;
        margin-bottom: 20px;
    }
    .status-box {
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Typography style rules */
    .brand-title { font-size: 32px; font-weight: 800; color: #1A202C; }
    .brand-green { color: #4FD1C5; }
    .subtitle-text { color: #718096; font-size: 15px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

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
            response = requests.post(url, json=json_data, timeout=3)
        else:
            response = requests.get(url, timeout=3)
        return response
    except Exception:
        return None


# ==============================================================================
# JALUR 1: HALAMAN LOGIN / SIGN UP (Sesuai Tampilan image_61aa43.png)
# ==============================================================================
if not st.session_state.authenticated:
    
    # Split Tampilan Kiri dan Kanan 50:50 sesuai Gambar Desain
    left_side, right_side = st.columns([1, 1], gap="large")
    
    with left_side:
        st.write("\n\n")
        # Logo Komponen
        st.markdown('### 🟢 KeepIn <span style="background-color:#E6FFFA; color:#4FD1C5; font-size:12px; padding:3px 8px; border-radius:5px; font-weight:bold;">Mitra</span>', unsafe_allow_html=True)
        st.write("")
        
        if st.session_state.auth_page == 'Login':
            st.markdown('<p class="brand-title">Selamat datang kembali! 👋</p>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle-text">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</p>', unsafe_allow_html=True)
            
            # Selector Role Sesuai Gambar Kotak Pilihan Peran
            st.write("**PILIH ROLE ANDA**")
            role_pilihan = st.radio("Role Selector", ["Mitra (Kelola loker bisnis)", "Penyewa (Booking loker mudah)", "Admin (Kelola sistem platform)"], label_visibility="collapsed")
            role_clean = "mitra" if "Mitra" in role_pilihan else "penyewa" if "Penyewa" in role_pilihan else "admin"
            
            st.write("")
            email_input = st.text_input("EMAIL", placeholder="Masukkan email Anda")
            password_input = st.text_input("KATA SANDI", type="password", placeholder="Masukkan kata sandi")
            
            st.checkbox("Ingat saya")
            st.write("")
            
            if st.button("Masuk ke Akun", use_container_width=True):
                if email_input and password_input:
                    # Tembak Endpoint Auth Service
                    res = fetch_data_from_service("auth", "/login", "POST", {"email": email_input, "password": password_input, "role": role_clean})
                    if res and res.status_code == 200:
                        login_res = res.json()
                        st.session_state.authenticated = True
                        st.session_state.user_info = login_res["user"]
                        st.success(f"Selamat Datang {login_res['user']['nama']}!")
                        st.rerun()
                    else:
                        st.error("Gagal Masuk: Email, Password, atau Peran Akun salah.")
                else:
                    st.warning("Mohon isi semua field login!")
                    
            st.markdown("---")
            st.write("Belum punya akun mitra?")
            if st.button("Daftar Akun Mitra Baru"):
                st.session_state.auth_page = 'SignUp'
                st.rerun()
                
        elif st.session_state.auth_page == 'SignUp':
            st.markdown('<p class="brand-title">Gabung Sebagai Mitra 🚀</p>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle-text">Mulai sediakan layanan loker pintar dan raih pendapatan pasif dengan mudah.</p>', unsafe_allow_html=True)
            
            reg_nama = st.text_input("NAMA LENGKAP PERUSAHAAN/INDIVIDU")
            reg_email = st.text_input("EMAIL AKTIF")
            reg_hp = st.text_input("NOMOR HANDPHONE")
            reg_pass = st.text_input("KATA SANDI BARU", type="password")
            
            if st.button("Daftarkan Kemitraan", use_container_width=True):
                if reg_nama and reg_email and reg_pass:
                    payload = {"nama": reg_nama, "email": reg_email, "password": reg_pass, "no_hp": reg_hp, "role": "mitra"}
                    res = fetch_data_from_service("auth", "/register", "POST", payload)
                    if res and res.status_code == 201:
                        st.success("Registrasi Berhasil! Silakan masuk.")
                        st.session_state.auth_page = 'Login'
                        st.rerun()
                    else:
                        st.error(res.json().get("message", "Gagal mendaftar."))
                else:
                    st.warning("Harap lengkapi formulir pendaftaran!")
            
            if st.button("Sudah punya akun? Login"):
                st.session_state.auth_page = 'Login'
                st.rerun()

    # Sisi Kanan: Panel Edukasi/Promosi Sesuai Desain image_61aa43.png
    with right_side:
        st.write("\n\n\n\n")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F0FDF4 0%, #E6FFFA 100%); padding: 50px; border-radius: 30px; border: 1px solid #DCFCE7;">
            <h1 style="font-size: 38px; font-weight: 800; color: #1A202C; line-height: 1.2;">
                Satu platform untuk <br><span style="color: #4FD1C5;">semua kebutuhan</span> loker.
            </h1>
            <p style="color: #4A5568; font-size: 16px; margin-top: 15px; margin-bottom: 40px;">
                Baik Anda mitra pemilik properti, penyewa yang sedang bepergian, atau admin platform. KeepIn siap mendigitalkan penitipan barang Anda.
            </p>
            
            <div style="margin-bottom: 25px;">
                <p style="font-weight: 700; color: #2D3748; margin: 0; font-size:16px;">🟢 Kelola Bisnis Lebih Mudah</p>
                <p style="color: #718096; margin: 0; font-size:14px;">Pantau pendapatan, kuota booking, dan performa IoT loker secara real-time.</p>
            </div>
            <div style="margin-bottom: 25px;">
                <p style="font-weight: 700; color: #2D3748; margin: 0; font-size:16px;">📦 Booking Cepat & Praktis</p>
                <p style="color: #718096; margin: 0; font-size:14px;">Cari loker terdekat yang kosong dan lakukan enkripsi kunci pesanan dalam hitungan detik.</p>
            </div>
            <div>
                <p style="font-weight: 700; color: #2D3748; margin: 0; font-size:16px;">🔒 Sistem Aman & Terpercaya</p>
                <p style="color: #718096; margin: 0; font-size:14px;">Data transaksi keuangan terintegrasi dengan payment gateway berstandar tinggi.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# JALUR 2: UTAMA CORE DASHBOARD (Sesuai Tampilan Ter-autentikasi image_61aa9b.png)
# ==============================================================================
else:
    # Ambil Status Real-Time dari Seluruh Microservices
    res_b = fetch_data_from_service("booking", "/booking")
    res_p = fetch_data_from_service("payment", "/payment")
    
    b_status = "Online" if res_b else "Offline"
    p_status = "Online" if res_p else "Offline"
    
    df_booking = pd.DataFrame(res_b.json()) if res_b and res_b.status_code == 200 else pd.DataFrame()
    df_payment = pd.DataFrame(res_p.json()) if res_p and res_p.status_code == 200 else pd.DataFrame()

    # Sidebar Navigasi Utama setelah Login
    with st.sidebar:
        st.markdown(f'### 🏢 KeepIn <span style="font-size:11px; background:#4FD1C5; color:white; padding:2px 6px; border-radius:4px;">{st.session_state.user_info["role"].upper()}</span>', unsafe_allow_html=True)
        st.write(f"Akun: **{st.session_state.user_info['nama']}**")
        st.markdown("---")
        
        st.button("🏠 Beranda", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Beranda"}))
        st.button("📋 Pendaftaran Usaha", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Pendaftaran"}))
        st.button("📊 Laporan Bisnis", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Laporan"}))
        st.markdown("---")
        
        # System status monitoring panel (Sesuai Gambar Sidebar Hijau image_61b985.png)
        st.write("**SYSTEM MONITORING**")
        for s_title, s_stat in [("Auth Service", "Online"), ("Booking Service", b_status), ("Payment Service", p_status)]:
            bg_box = "#DEF7EC" if s_stat == "Online" else "#FDE8E8"
            tx_box = "#03543F" if s_stat == "Online" else "#9B1C1C"
            st.markdown(f'<div class="status-box" style="background-color: {bg_box}; color: {tx_box};">● {s_title}: {s_stat}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("⬅️ Keluar / Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    # TAMPILAN HALAMAN BERANDA MITRA (Sesuai image_61aa9b.png)
    if st.session_state.dashboard_page == 'Beranda':
        top_left, top_right = st.columns([3, 1])
        with top_left:
            st.markdown(f'<p class="brand-title">Selamat datang kembali, {st.session_state.user_info["nama"]}! 👋</p>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle-text">Kelola usaha dan pantau performa loker Anda dengan mudah.</p>', unsafe_allow_html=True)
        with top_right:
            st.selectbox("FILTER USAHA", ["Semua Usaha", "Cabang Gambir", "Cabang Sudirman"], label_visibility="collapsed")

        # Banner Daftarkan Usaha Baru
        st.markdown("""
            <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 5px solid #4FD1C5;">
                <div>
                    <p style="font-size: 18px; font-weight: 700; margin: 0; color: #2D3748;">Daftarkan Usaha Baru</p>
                    <p style="font-size: 13px; color: #718096; margin: 0;">Tambahkan lokasi usaha Anda untuk mulai menyewakan slot unit loker pintar.</p>
                </div>
                <div style="background-color: #1A202C; color: white; padding: 10px 20px; border-radius: 10px; font-weight: 700; font-size: 13px;">
                    DAFTARKAN SEKARANG
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Seksi Grid Statistik Utama
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:12px; font-weight:700;">TOTAL USAHA</p><h2>3</h2><p style="color:#48BB78; font-size:12px;">↑ +12% vs bulan lalu</p></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:12px; font-weight:700;">TOTAL LOKER</p><h2>48</h2><p style="color:#48BB78; font-size:12px;">↑ +12% vs bulan lalu</p></div>', unsafe_allow_html=True)
        with col_m3:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:12px; font-weight:700;">LOKER AKTIF</p><h2>36</h2><p style="color:#48BB78; font-size:12px;">↑ +12% vs bulan lalu</p></div>', unsafe_allow_html=True)
        with col_m4:
            total_b = len(df_booking) if not df_booking.empty else 128
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:12px; font-weight:700;">TOTAL BOOKING</p><h2>{total_b}</h2><p style="color:#48BB78; font-size:12px;">↑ +12% vs bulan lalu</p></div>', unsafe_allow_html=True)

        # Tabel Daftar Usaha Saya
        st.write("### DAFTAR USAHA SAYA")
        mock_table = pd.DataFrame({
            "PROFIL USAHA": ["KeepIn Stasiun Gambir", "KeepIn Grand Indonesia Mall", "KeepIn Bandara Soetta T3"],
            "TOTAL LOKER": [20, 15, 13],
            "LOKER AKTIF": [18, 12, 6],
            "TOTAL BOOKING": [45, 30, 53]
        })
        st.dataframe(mock_table, use_container_width=True, hide_index=True)

    # TAMPILAN HALAMAN LAPORAN BISNIS
    elif st.session_state.dashboard_page == 'Laporan':
        st.markdown('<p class="brand-title">Laporan Performa Bisnis 📈</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle-text">Informasi riwayat pendapatan dari agregasi Payment Gateway Service.</p>', unsafe_allow_html=True)
        
        if not df_payment.empty:
            st.write("### LOG TRANSAKSI KEUANGAN ASLI (MICROSERVICE)")
            st.dataframe(df_payment, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pembayaran real-time yang tercatat di payment_service.")