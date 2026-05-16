import streamlit as st
import pandas as pd
import requests

# --- 1. SET CONFIG & INJECT CSS GAYA PREMIUM (WEB-OPTIMIZED) ---
st.set_page_config(page_title="KeepIn Console", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS untuk merombak total tampilan default Streamlit
st.markdown("""
    <style>
    /* Menghilangkan padding bawaan Streamlit agar layout full-width */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    
    /* Global Background */
    .stApp { background-color: #FFFFFF; }
    
    /* Menghilangkan border & padding default column Streamlit */
    div[data-testid="column"] { padding: 0px !important; }
    
    /* Custom Card & Interactive Element Styling */
    .role-box-active {
        border: 2px solid #4FD1C5;
        background-color: #F0FDF4;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
    }
    .role-box-inactive {
        border: 1px solid #E2E8F0;
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        border: 1px solid #F1F5F9;
    }
    .status-box {
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Modifikasi tombol default Streamlit agar match dengan design system */
    .stButton>button {
        background-color: #1A202C;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover { background-color: #2D3748; color: white; }
    
    /* Tombol sekunder / link */
    div.sub-btn > div > button {
        background-color: transparent !important;
        color: #4FD1C5 !important;
        border: none !important;
        text-decoration: underline;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MANAGEMENT SESSION STATE ---
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
# VIEW JALUR 1: SISTEM AUTENTIKASI (SPLIT SCREEN SEMPURNA 50:50)
# ==============================================================================
if not st.session_state.authenticated:
    
    if st.session_state.auth_page == 'Login':
        # --- HALAMAN LOGIN (Sesuai image_614d20.png / image_61aa43.png) ---
        col_form, col_banner = st.columns([1, 1])
        
        with col_form:
            # Padding container dalam agar form presisi di tengah
            st.markdown('<div style="padding: 60px 10% 40px 12%;">', unsafe_allow_html=True)
            st.markdown('### 🟢 KeepIn <span style="background-color:#E6FFFA; color:#4FD1C5; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:bold;">Mitra</span>', unsafe_allow_html=True)
            st.write("\n")
            st.markdown('<h1 style="font-size: 32px; font-weight:800; margin-bottom:5px;">Selamat datang kembali! 👏</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px; margin-bottom:30px;">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</p>', unsafe_allow_html=True)
            
            # KOTAK PILIHAN ROLE (3 Grid Horizontal)
            st.markdown('<p style="font-size:12px; font-weight:700; color:#4A5568; letter-spacing:0.5px;">PILIH ROLE ANDA</p>', unsafe_allow_html=True)
            r_col1, r_col2, r_col3 = st.columns(3)
            
            with r_col1:
                active_class = "role-box-active" if st.session_state.selected_role == 'mitra' else "role-box-inactive"
                st.markdown(f'<div class="{active_class}">📦<br><b>Mitra</b><br><span style="font-size:10px; color:#718096;">Kelola loker bisnis</span></div>', unsafe_allow_html=True)
                if st.button("Pilih Mitra", key="btn_role_m", use_container_width=True):
                    st.session_state.selected_role = 'mitra'
                    st.rerun()
            with r_col2:
                active_class = "role-box-active" if st.session_state.selected_role == 'penyewa' else "role-box-inactive"
                st.markdown(f'<div class="{active_class}">🎒<br><b>Penyewa</b><br><span style="font-size:10px; color:#718096;">Booking loker mudah</span></div>', unsafe_allow_html=True)
                if st.button("Pilih Penyewa", key="btn_role_p", use_container_width=True):
                    st.session_state.selected_role = 'penyewa'
                    st.rerun()
            with r_col3:
                active_class = "role-box-active" if st.session_state.selected_role == 'admin' else "role-box-inactive"
                st.markdown(f'<div class="{active_class}">🛡️<br><b>Admin</b><br><span style="font-size:10px; color:#718096;">Sistem platform</span></div>', unsafe_allow_html=True)
                if st.button("Pilih Admin", key="btn_role_a", use_container_width=True):
                    st.session_state.selected_role = 'admin'
                    st.rerun()
            
            st.write("\n")
            email = st.text_input("EMAIL", placeholder="Masukkan email Anda")
            password = st.text_input("KATA SANDI", type="password", placeholder="Masukkan kata sandi")
            
            st.checkbox("Ingat saya", key="remember_me")
            st.write("\n")
            
            if st.button("Masuk ke Akun", key="submit_login", use_container_width=True):
                if email and password:
                    res = fetch_data_from_service("auth", "/login", "POST", {"email": email, "password": password, "role": st.session_state.selected_role})
                    if res and res.status_code == 200:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res.json()["user"]
                        st.rerun()
                    else:
                        st.error("Kredensial salah atau tidak cocok dengan role terpilih.")
                else:
                    st.warning("Harap isi seluruh kolom email dan kata sandi.")
            
            st.write("\n")
            st.markdown('<p style="text-align:center; font-size:13px; color:#718096;">Belum punya akun mitra?</p>', unsafe_allow_html=True)
            st.markdown('<div class="sub-btn">', unsafe_allow_html=True)
            if st.button("Daftar Akun Kemitraan Baru", key="goto_signup"):
                st.session_state.auth_page = 'SignUp'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_banner:
            # BANNER KANAN EDUKASI (Sesuai Info Box Hijau Halus)
            st.markdown("""
                <div style="background: linear-gradient(135deg, #F0FDF4 0%, #E6FFFA 100%); height: 100vh; padding: 100px 12% 40px 12%; border-left: 1px solid #E2E8F0;">
                    <h1 style="font-size: 42px; font-weight: 800; color: #1A202C; line-height: 1.25; margin-bottom:20px;">
                        Satu platform untuk <br><span style="color: #4FD1C5;">semua kebutuhan</span> loker.
                    </h1>
                    <p style="color: #4A5568; font-size: 15px; margin-bottom: 50px; line-height:1.6;">
                        Baik Anda mitra pemilik properti, penyewa yang sedang bepergian, atau admin platform. KeepIn siap mendigitalkan penitipan barang Anda secara aman.
                    </p>
                    
                    <div style="margin-bottom: 30px;">
                        <h4 style="margin:0 0 5px 0; color:#2D3748; font-size:16px;">🟢 Kelola Bisnis Lebih Mudah</h4>
                        <p style="margin:0; color:#718096; font-size:14px;">Pantau pendapatan, kuota booking, dan performa IoT loker secara real-time.</p>
                    </div>
                    <div style="margin-bottom: 30px;">
                        <h4 style="margin:0 0 5px 0; color:#2D3748; font-size:16px;">📦 Booking Cepat & Praktis</h4>
                        <p style="margin:0; color:#718096; font-size:14px;">Cari loker terdekat yang kosong dan lakukan enkripsi kunci pesanan dalam hitungan detik.</p>
                    </div>
                    <div>
                        <h4 style="margin:0 0 5px 0; color:#2D3748; font-size:16px;">🔒 Sistem Aman & Terpercaya</h4>
                        <p style="margin:0; color:#718096; font-size:14px;">Data transaksi keuangan terintegrasi dengan payment gateway berstandar tinggi.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.auth_page == 'SignUp':
        # --- HALAMAN REGISTER/SIGNUP (Sesuai image_614fe8.png - Dark Theme Left Side) ---
        col_dark_banner, col_reg_form = st.columns([1, 1])
        
        with col_dark_banner:
            st.markdown("""
                <div style="background-color: #1A202C; color: white; height: 100vh; padding: 100px 12% 40px 12%; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h3 style="color:#4FD1C5; margin-bottom:40px;">🟢 KeepIn Console</h3>
                        <h1 style="font-size: 40px; font-weight: 800; line-height: 1.3; margin-bottom:20px;">Mulai kelola loker Anda dengan profesional.</h1>
                        <p style="color:#A0AEC0; font-size:15px; line-height:1.6; margin-bottom:40px;">Bergabunglah dengan ribuan mitra dan penyewa yang mempercayakan keamanan barang mereka pada KeepIn.</p>
                        
                        <div style="margin-bottom:25px;">
                            <span style="color:#4FD1C5; font-weight:bold;">⊙ Infrastruktur Kuat:</span> Bekerja dengan PostgreSQL untuk integritas data maksimal.
                        </div>
                        <div style="margin-bottom:25px;">
                            <span style="color:#4FD1C5; font-weight:bold;">⊙ Keamanan Berlapis:</span> Sistem otentikasi aman dan pemantauan real-time.
                        </div>
                        <div>
                            <span style="color:#4FD1C5; font-weight:bold;">⊙ Skalabilitas Tinggi:</span> Siap mendukung pertumbuhan bisnis Anda dari satu hingga ribuan loker.
                        </div>
                    </div>
                    <div>
                        <p style="color:#718096; font-size:12px; margin:0;">PLATFORM STATUS</p>
                        <p style="color:#48BB78; font-size:13px; font-weight:bold; margin:0;">● Sistem Berjalan - v1.0.4 Production</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_reg_form:
            st.markdown('<div style="padding: 60px 15% 40px 12%;">', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px; margin:0;">← KEMBALI KE LOGIN</p>', unsafe_allow_html=True)
            if st.button("Kembali", key="back_to_login_top"):
                st.session_state.auth_page = 'Login'
                st.rerun()
                
            st.markdown('<h1 style="font-size: 32px; font-weight:800; margin-top:20px; margin-bottom:5px;">Daftar Akun Baru</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px; margin-bottom:35px;">Lengkapi data berikut untuk bergabung dengan KeepIn.</p>', unsafe_allow_html=True)
            
            # Toggle Button Peran di Form Pendaftaran
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.markdown('<div class="role-box-active" style="padding:10px;">Mitra</div>', unsafe_allow_html=True)
            with t_col2:
                st.markdown('<div class="role-box-inactive" style="padding:10px; color:#A0AEC0;">Penyewa</div>', unsafe_allow_html=True)
                
            st.write("\n")
            reg_nama = st.text_input("NAMA LENGKAP", placeholder="Contoh: Andi Pratama")
            
            c_input1, c_input2 = st.columns(2)
            with c_input1:
                reg_email = st.text_input("EMAIL", placeholder="nama@email.com")
            with c_input2:
                reg_hp = st.text_input("NO. TELP", placeholder="081234567XXX")
                
            reg_pass = st.text_input("KATA SANDI", type="password", placeholder="Minimal 8 karakter")
            
            st.markdown('<p style="font-size:11px; color:#A0AEC0; margin-top:10px;">Dengan mendaftar, Anda menyetujui Syarat & Ketentuan serta Kebijakan Privasi kami.</p>', unsafe_allow_html=True)
            st.write("\n")
            
            if st.button("Daftar Akun", key="submit_register"):
                if reg_nama and reg_email and reg_pass:
                    payload = {"nama": reg_nama, "email": reg_email, "password": reg_pass, "no_hp": reg_hp, "role": "mitra"}
                    res = fetch_data_from_service("auth", "/register", "POST", payload)
                    if res and res.status_code == 201:
                        st.success("Akun berhasil dibuat! Silakan masuk.")
                        st.session_state.auth_page = 'Login'
                        st.rerun()
                    else:
                        st.error("Registrasi gagal. Email mungkin sudah terdaftar.")
                else:
                    st.warning("Mohon isi semua data wajib pendaftaran.")
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# VIEW JALUR 2: CORE WORKSPACE DASHBOARD (SETELAH BERHASIL LOGIN)
# ==============================================================================
else:
    # Mengambil status kesehatan & data dari microservices backend
    res_b = fetch_data_from_service("booking", "/booking")
    res_p = fetch_data_from_service("payment", "/payment")
    
    b_status = "Online" if res_b else "Offline"
    p_status = "Online" if res_p else "Offline"
    
    df_booking = pd.DataFrame(res_b.json()) if res_b and res_b.status_code == 200 else pd.DataFrame()
    df_payment = pd.DataFrame(res_p.json()) if res_p and res_p.status_code == 200 else pd.DataFrame()

    # Tampilkan Sidebar Khusus Konsol Mitra (Sesuai image_61b985.png)
    with st.sidebar:
        st.markdown(f'### 🏢 KeepIn <span style="font-size:11px; background:#4FD1C5; color:white; padding:2px 6px; border-radius:4px;">{st.session_state.user_info["role"].upper()}</span>', unsafe_allow_html=True)
        st.write(f"Akun Aktif: **{st.session_state.user_info['nama']}**")
        st.markdown("---")
        
        st.button("🏠 Beranda", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Beranda"}))
        st.button("📋 Pendaftaran Usaha", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Pendaftaran"}))
        st.button("📊 Laporan Bisnis", use_container_width=True, on_click=lambda: st.session_state.update({"dashboard_page": "Laporan"}))
        st.markdown("---")
        
        st.write("**SYSTEM STATUS**")
        for s_title, s_stat in [("Auth Service", "Online"), ("Booking Service", b_status), ("Payment Service", p_status)]:
            bg_box = "#DEF7EC" if s_stat == "Online" else "#FDE8E8"
            tx_box = "#03543F" if s_stat == "Online" else "#9B1C1C"
            st.markdown(f'<div class="status-box" style="background-color: {bg_box}; color: {tx_box};">● {s_title}: {s_stat}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("⬅️ Keluar / Logout", use_container_width=True, key="logout_app"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    # --- KONTEN CORE DASHBOARD (Sesuai image_61aa9b.png) ---
    st.markdown('<div style="padding: 30px 40px;">', unsafe_allow_html=True)
    
    if st.session_state.dashboard_page == 'Beranda':
        # Header Atas
        top_left, top_right = st.columns([3, 1])
        with top_left:
            st.markdown(f'<h1 style="font-size:28px; font-weight:800; margin:0;">Selamat datang kembali, {st.session_state.user_info["nama"]}! 👋</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color:#718096; font-size:14px;">Kelola usaha dan pantau performa loker Anda dengan mudah.</p>', unsafe_allow_html=True)
        with top_right:
            st.selectbox("FILTER USAHA", ["Semua Usaha", "Cabang Gambir"], label_visibility="collapsed")

        st.write("\n")
        # Banner Daftarkan Usaha
        st.markdown("""
            <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #4FD1C5;">
                <div>
                    <h4 style="margin: 0 0 4px 0; color: #2D3748; font-size:16px;">Daftarkan Usaha Baru</h4>
                    <p style="font-size: 13px; color: #718096; margin: 0;">Tambahkan lokasi usaha Anda untuk mulai menyewakan slot unit loker pintar.</p>
                </div>
                <div style="background-color: #1A202C; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700; font-size: 12px; cursor:pointer;">
                    DAFTARKAN SEKARANG
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("\n")
        # Grid Metrik Angka Utama
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL USAHA</p><h2 style="margin:5px 0;">3</h2><p style="color:#48BB78; font-size:11px; margin:0;">↑ +12% vs last month</p></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL LOKER</p><h2 style="margin:5px 0;">48</h2><p style="color:#48BB78; font-size:11px; margin:0;">↑ +12% vs last month</p></div>', unsafe_allow_html=True)
        with col_m3:
            st.markdown('<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">LOKER AKTIF</p><h2 style="margin:5px 0;">36</h2><p style="color:#48BB78; font-size:11px; margin:0;">↑ +12% vs last month</p></div>', unsafe_allow_html=True)
        with col_m4:
            total_b = len(df_booking) if not df_booking.empty else 128
            st.markdown(f'<div class="metric-card"><p style="color:#718096; font-size:11px; font-weight:700; margin:0;">TOTAL BOOKING</p><h2 style="margin:5px 0;">{total_b}</h2><p style="color:#48BB78; font-size:11px; margin:0;">↑ +12% vs last month</p></div>', unsafe_allow_html=True)

        st.write("\n\n")
        st.markdown('<p style="font-size:13px; font-weight:700; color:#718096; letter-spacing:0.5px;">DAFTAR USAHA SAYA</p>', unsafe_allow_html=True)
        
        mock_table = pd.DataFrame({
            "PROFIL USAHA": ["KeepIn Stasiun Gambir", "KeepIn Grand Indonesia Mall", "KeepIn Bandara Soetta T3"],
            "TOTAL LOKER": [20, 15, 13],
            "LOKER AKTIF": [18, 12, 6],
            "TOTAL BOOKING": [45, 30, 53]
        })
        st.dataframe(mock_table, use_container_width=True, hide_index=True)

    elif st.session_state.dashboard_page == 'Laporan':
        st.markdown('<h1 style="font-size:28px; font-weight:800;">Laporan Performa Bisnis 📊</h1>', unsafe_allow_html=True)
        if not df_payment.empty:
            st.write(df_payment)
        else:
            st.info("Menunggu transaksi dari payment_service.")
            
    st.markdown('</div>', unsafe_allow_html=True)