# app.py
from PIL import Image
import streamlit as st
import requests
from io import BytesIO
import base64

# URL Endpoints Microservice Auth
AUTH_LOGIN_URL = "http://127.0.0.1:8000/api/auth/login"
AUTH_REGISTER_URL = "http://127.0.0.1:8000/api/auth/register"
BOOKING_SERVICE_URL = "http://127.0.0.1:8001/api/booking"
LOKER_SERVICE_URL = "http://127.0.0.1:8002/api/loker"

try:
    icon_img = Image.open("./src/images/icon.png")
    st.set_page_config(page_title="KeepIn - Platform Loker", page_icon=icon_img, layout="wide", initial_sidebar_state="collapsed")
except:
    st.set_page_config(page_title="KeepIn - Platform Loker", layout="wide", initial_sidebar_state="collapsed")

# ==============================================================================
# INITIALIZATION STATES (SISTEM NAVIGASI & SESSION)
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# Default menu internal ketika pertama kali masuk dashboard
if "active_menu" not in st.session_state:
    st.session_state["active_menu"] = "Beranda"

# Cari area inisialisasi state, tambahkan:
if "id_user" not in st.session_state:
    st.session_state["id_user"] = None

# Helper konversi gambar ke base64 untuk kustom HTML
def image_to_base64(img_path):
    try:
        img = Image.open(img_path)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except:
        return None

logo_base64 = image_to_base64("./src/images/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="30">' if logo_base64 else '🟢'

# --- Custom Global UI CSS ---
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


# ==============================================================================
# VIEW 1: AUTHENTICATION (LOGIN)
# ==============================================================================
if st.session_state["current_page"] == "login":
    col_left, col_space, col_right = st.columns([1.2, 0.2, 1.2])

    with col_left:
        st.markdown(f'<div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">{logo_html}<span style="font-size:24px; font-weight:bold; color:#1E293B;">KeepIn</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Selamat datang kembali! 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-label">Pilih Role Anda</div>', unsafe_allow_html=True)
        selected_role = st.radio("Role", ["Penyewa", "Mitra", "Admin"], horizontal=True, label_visibility="collapsed")
        
        st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
        email = st.text_input("Email Login", placeholder="Masukkan email Anda", label_visibility="collapsed")
        
        st.markdown('<div class="form-label">Kata Sandi</div>', unsafe_allow_html=True)
        password = st.text_input("Kata Sandi Login", type="password", placeholder="Masukkan kata sandi", label_visibility="collapsed")
        
        col_p1, col_p2 = st.columns([1, 1])
        with col_p1: st.checkbox("Ingat saya")
        with col_p2: st.markdown("<p style='text-align: right; margin-top: 4px;'><a href='#' style='color:#52D1A2; font-size:14px; text-decoration:none; font-weight:600;'>Lupa kata sandi?</a></p>", unsafe_allow_html=True)
            
        st.markdown('<div class="login-btn-container">', unsafe_allow_html=True)
        if st.button("Masuk ke Akun"):
            if not email or not password:
                st.warning("Harap isi Email dan Kata Sandi terlebih dahulu!")
            else:
                payload = {"email": email, "password": password, "role": selected_role}
                try:
                    response = requests.post(AUTH_LOGIN_URL, json=payload)
                    res_data = response.json() if response.headers.get('content-type') == 'application/json' else None
                    
                    if response.status_code == 200 and res_data:
                        # SET SESSION STATE APABILA LOGIN SUKSES
                        st.session_state["token"] = res_data["token"]
                        st.session_state["user_email"] = res_data["user"]["email"]
                        st.session_state["user_role"] = res_data["user"]["role"] # 'Penyewa', 'Mitra', atau 'Admin'
                        st.session_state["id_user"] = res_data["user"]["id_user"] # <--- SIMPAN ID USER
                        # REDIRECT SESUAI ROLE KLIEN
                        st.session_state["current_page"] = "dashboard"
                        st.session_state["active_menu"] = "Beranda" # Reset menu utama
                        st.rerun()
                    else:
                        error_msg = res_data.get('detail', 'Terjadi kesalahan internal') if res_data else response.text
                        st.error(f"❌ Login Gagal: {error_msg}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Gagal terhubung ke `auth_service.py`. Pastikan backend service sudah dinyalakan!")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("Belum punya akun? Daftar sekarang", key="go_to_register_btn"):
            st.session_state["current_page"] = "register"
            st.rerun()

    with col_right:
        st.write("##")
        st.markdown('<div class="right-title">Satu platform untuk <br><span class="highlight-text">semua kebutuhan loker.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="right-subtitle">Baik Anda mitra, penyewa, atau admin. KeepIn siap membantu.</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-1">🟢</div><div><div class="feature-title">Kelola Bisnis Lebih Mudah</div><div class="feature-desc">Pantau pendapatan, booking, dan performa loker secara real-time.</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-2">🔵</div><div><div class="feature-title">Booking Cepat & Praktis</div><div class="feature-desc">Cari loker terdekat dan booking dalam hitungan detik.</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-3">🟠</div><div><div class="feature-title">Sistem Aman & Terpercaya</div><div class="feature-desc">Data Anda terlindungi dengan enkripsi berstandar tinggi.</div></div></div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 2: AUTHENTICATION (REGISTER)
# ==============================================================================
elif st.session_state["current_page"] == "register":
    col_reg_left, col_reg_space, col_reg_right = st.columns([1.2, 0.1, 1.3])
    
    with col_reg_left:
        st.markdown("""
            <div style="background-color: #1E293B; padding: 40px; border-radius: 16px; color: white; min-height: 550px;">
                <h2 style='color: white; font-weight: 800;'>Mulai kelola loker Anda dengan profesional.</h2>
                <p style='color: #94A3B8; font-size: 14px;'>Bergabunglah dengan ribuan mitra dan penyewa yang mempercayakan keamanan barang mereka pada KeepIn.</p>
                <br><br>
                <div style='margin-bottom:20px;'><b>🟢 Infrastruktur Kuat</b><br><small style='color:#94A3B8;'>Bekerja dengan database andal untuk integritas data maksimal.</small></div>
                <div style='margin-bottom:20px;'><b>🔒 Keamanan Berlapis</b><br><small style='color:#94A3B8;'>Sistem otentikasi aman dan pemantauan real-time.</small></div>
                <div><b>🚀 Skalabilitas Tinggi</b><br><small style='color:#94A3B8;'>Siap mendukung pertumbuhan bisnis Anda dari satu hingga ribuan loker.</small></div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_reg_right:
        if st.button("⬅ KEMBALI KE LOGIN", key="back_to_login_top"):
            st.session_state["current_page"] = "login"
            st.rerun()
            
        st.markdown('<div class="welcome-title" style="margin-top:15px;">Daftar Akun Baru</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Lengkapi data berikut untuk bergabung dengan KeepIn.</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-label">Pilih Jenis Akun</div>', unsafe_allow_html=True)
        reg_role = st.radio("Reg Role", ["Penyewa", "Mitra"], horizontal=True, label_visibility="collapsed")
        
        st.markdown('<div class="form-label">Nama Lengkap</div>', unsafe_allow_html=True)
        nama_lengkap = st.text_input("Reg Nama", placeholder="Contoh: Andi Pratama", label_visibility="collapsed")
        
        col_input_1, col_input_2 = st.columns(2)
        with col_input_1:
            st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
            reg_email = st.text_input("Reg Email", placeholder="nama@email.com", label_visibility="collapsed")
        with col_input_2:
            st.markdown('<div class="form-label">No. Telp</div>', unsafe_allow_html=True)
            reg_telp = st.text_input("Reg Telp", placeholder="081234567XXX", label_visibility="collapsed")
            
        st.markdown('<div class="form-label">Kata Sandi</div>', unsafe_allow_html=True)
        reg_password = st.text_input("Reg Password", type="password", placeholder="Minimal 8 karakter", label_visibility="collapsed")
        
        st.markdown("<small style='color:#64748B;'>Dengan mendaftar, Anda menyetujui Syarat & Ketentuan serta Kebijakan Privasi kami.</small>", unsafe_allow_html=True)
        
        if st.button("Daftar Akun", type="primary"):
            if not nama_lengkap or not reg_email or not reg_password:
                st.warning("Harap lengkapi semua kolom pendaftaran yang wajib!")
            else:
                payload = {
                    "nama_lengkap": nama_lengkap,
                    "email": reg_email,
                    "no_telp": reg_telp if reg_telp else "-",
                    "password": reg_password,
                    "role": reg_role
                }
                try:
                    response = requests.post(AUTH_REGISTER_URL, json=payload)
                    res_data = response.json()
                    
                    if response.status_code == 201:
                        st.success(f"🎉 {res_data['message']}")
                        st.balloons()
                        st.info("Silakan klik 'Kembali ke Login' untuk mencoba akun baru Anda.")
                    else:
                        st.error(f"❌ Registrasi Gagal: {res_data.get('detail', 'Terjadi kesalahan')}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Gagal terhubung ke server auth backend.")


# ==============================================================================
# VIEW 3: MAIN INTERNAL DASHBOARD SYSTEM (MULTI-ROLE)
# ==============================================================================
elif st.session_state["current_page"] == "dashboard":
    role_aktif = st.session_state["user_role"]
    email_user = st.session_state["user_email"]

    # 1. SIDEBAR DYNAMIC ROUTING BERDASARKAN ROLE
    with st.sidebar:
        st.markdown(f'<div style="display:flex; align-items:center; gap:10px; margin-bottom: 25px;">{logo_html}<span style="font-size:22px; font-weight:bold; color:#1E293B;">KeepIn <small style="font-size:10px; background:#EEF2FF; color:#4F46E5; padding:2px 6px; border-radius:4px;">{role_aktif.upper()}</small></span></div>', unsafe_allow_html=True)
        st.write(f"📧 `{email_user}`")
        st.write("---")
        
        # --- PERBAIKAN NO 3: PENENTUAN LIST MENU BERDASARKAN ROLE ---
        if role_aktif.lower() == "penyewa":
            list_menu = ["Beranda", "Booking", "Riwayat Booking", "Notifikasi", "Info Promo"]
        elif role_aktif.lower() == "mitra":
            list_menu = ["Beranda", "Pendaftaran Usaha", "Laporan Bisnis", "Aktivitas Loker", "Penarikan Saldo"]
        else: # Default fallback Admin
            list_menu = ["Beranda", "Manajemen User", "Sistem Server"]
            
        # VALIDASI AMAN: Mencegah ValueError jika active_menu sebelumnya tidak ada di dalam list_menu role baru
        if st.session_state["active_menu"] not in list_menu:
            st.session_state["active_menu"] = list_menu[0]

        # Tampilkan Navigasi Menu Radio dengan mencocokkan index terkini di session_state
        pilihan_nav = st.radio(
            "MAIN MENU", 
            list_menu, 
            index=list_menu.index(st.session_state["active_menu"])
        )
        st.session_state["active_menu"] = pilihan_nav
        
        st.write("---")
        if st.button("🚪 Keluar / Logout", key="logout_btn"):
            st.session_state["current_page"] = "login"
            st.session_state["user_role"] = None
            st.session_state["user_email"] = None
            st.session_state["id_user"] = None
            st.session_state["active_menu"] = "Beranda"
            st.rerun()

    # 2. RENDER KONTEN DASHBOARD BERDASARKAN MENUNYA
    menu_aktif = st.session_state["active_menu"]
    
    # ---------------- KONTEN KHUSUS: ROLE PENYEWA ----------------
    if role_aktif.lower() == "penyewa":
        st.title(f"💼 Portal {role_aktif} — {menu_aktif}")
        
        if menu_aktif == "Beranda":
            st.markdown(f"### Selamat datang kembali, {st.session_state['user_email']}! 👋")
            st.info("💡 Pilih menu **Booking** di sidebar kiri Anda untuk mulai mencari dan menyewa loker terdekat.")
            
        # ==================== KONTEN MENU BOOKING =======================================
        elif menu_aktif == "Booking":
            # State internal khusus alur booking agar halaman stabil saat rendering
            if "booking_step" not in st.session_state:
                st.session_state["booking_step"] = 1

            # --- CSS Kustom Tambahan untuk Desain Grid & Card UI Loker ---
            st.markdown("""
                <style>
                .loker-card {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
                    transition: transform 0.2s, border-color 0.2s;
                }
                .loker-card:hover {
                    transform: translateY(-2px);
                    border-color: #52D1A2;
                }
                .loker-title { font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
                .loker-size { font-size: 13px; color: #64748B; font-weight: 600; text-transform: uppercase; margin-bottom: 15px; }
                .loker-price { font-size: 20px; font-weight: 800; color: #52D1A2; margin-bottom: 5px; }
                .loker-unit { font-size: 12px; color: #94A3B8; }
                
                /* Ringkasan Pembayaran */
                .summary-card {
                    background-color: #F8FAFC;
                    border-radius: 12px;
                    padding: 20px;
                    border: 1px solid #E2E8F0;
                }
                .summary-row {
                    display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; color: #475569;
                }
                .summary-total {
                    display: flex; justify-content: space-between; margin-top: 15px; padding-top: 15px;
                    border-top: 1px dashed #CBD5E1; font-size: 18px; font-weight: 700; color: #1E293B;
                }
                </style>
            """, unsafe_allow_html=True)

            # ------------------------------------------------------------------
            # MOCKUP PAGE 1: PEMILIHAN UNIT LOKER
            # ------------------------------------------------------------------
            if st.session_state["booking_step"] == 1:
                st.markdown('<div class="welcome-title">Cari & Pesan Loker Strategis 📍</div>', unsafe_allow_html=True)
                st.markdown('<div class="welcome-subtitle">Temukan tempat penitipan barang terbaik dengan sistem keamanan digital 24 jam.</div>', unsafe_allow_html=True)
                
                # Filter Area Pencarian (Mockup Atas)
                col_f1, col_f2 = st.columns([2, 1])
                with col_f1:
                    lokasi_pilihan = st.selectbox("Pilih Lokasi / Mall terdekat:", ["Kuningan City Mall, Jakarta Selatan", "Mall Ambasador, Jakarta Selatan", "Kota Kasablanka, Jakarta Selatan"])
                with col_f2:
                    st.write("##") # Spacer penjajaran
                    st.button("🔍 Perbarui Lokasi", use_container_width=True)
                
                st.markdown("---")
                st.markdown(f"### 📦 Unit Loker Tersedia di **{lokasi_pilihan.split(',')[0]}**")
                st.write("")

                # --- PROSES AMBIL DATA DINAMIS DARI LOKER_SERVICE ---
                try:
                    response = requests.get(LOKER_SERVICE_URL, params={"lokasi": lokasi_pilihan})
                    
                    if response.status_code == 200:
                        daftar_loker = response.json().get("data", [])
                        
                        if not daftar_loker:
                            st.warning(f"⚠️ Maaf, saat ini tidak ada unit loker yang siap ('READY') di {lokasi_pilihan}.")
                        else:
                            cols = st.columns(3)
                            for idx, loker in enumerate(daftar_loker):
                                col_aktif = cols[idx % 3]
                                
                                with col_aktif:
                                    # Menampilkan data berdasarkan nama kolom baru database Anda
                                    st.markdown(f"""
                                        <div class="loker-card">
                                            <div class="loker-title">📦 Unit {loker['id_loker']}</div>
                                            <div class="loker-size">Tipe: {loker['tipe_loker']}</div>
                                            <div class="loker-price">Rp {loker['harga_per_jam']:,.0f}</div>
                                            <div class="loker-unit">per jam</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    st.write("")
                                    
                                    if st.button(f"Pilih & Sewa {loker['id_loker']}", use_container_width=True, key=f"btn_{loker['id_loker']}"):
                                        st.session_state["temp_id_loker"] = loker['id_loker']
                                        st.session_state["temp_tipe"] = loker['tipe_loker']
                                        st.session_state["temp_harga"] = loker['harga_per_jam']
                                        st.session_state["temp_lokasi"] = loker['lokasi']
                                        st.session_state["booking_step"] = 2
                                        st.rerun()
                    else:
                        st.error("❌ Gagal memuat data dari Loker Service.")
                except Exception as e:
                    st.error("❌ Gagal terhubung ke `loker_service.py`. Pastikan service Port 8002 aktif!")

            # ------------------------------------------------------------------
            # MOCKUP PAGE 2: FORMULIR DETAIL, DURASI & METODE PEMBAYARAN
            # ------------------------------------------------------------------
            elif st.session_state["booking_step"] == 2:
                if st.button("⬅ Kembali Pilih Loker", key="back_to_step1"):
                    st.session_state["booking_step"] = 1
                    st.rerun()
                
                st.markdown(f'<div class="welcome-title" style="margin-top:10px;">Konfirmasi Penyewaan Loker {st.session_state["temp_id_loker"]} 📝</div>', unsafe_allow_html=True)
                st.write("")

                # Split layout figma: Sisi kiri peta & konfigurasi, Sisi kanan ringkasan harga
                col_det_left, col_det_right = st.columns([1.3, 1])

                with col_det_left:
                    st.markdown("#### 📍 Lokasi Penempatan Fisik Loker")
                    # Embed Google Maps interaktif tiruan figma untuk Kuningan City Mall
                    st.markdown("""
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.307222459998!2d106.8277259747506!3d-6.223165260950669!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f3f4b5003b57%3A0x6bda19a9cf582!2sKuningan%20City!5e0!3m2!1sid!2sid!4v1710000000000!5m2!1sid!2sid" 
                        width="100%" height="220" style="border:0; border-radius:12px; margin-bottom:20px;" allowfullscreen="" loading="lazy"></iframe>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### 📆 Atur Durasi Penggunaan")
                    durasi = st.number_input("Berapa hari Anda ingin menyewa loker ini?", min_value=1, max_value=30, value=1, step=1)
                    
                    st.markdown("#### 💳 Metode Pembayaran")
                    metode_bayar = st.radio("Pilih Opsi Pembayaran:", ["QRIS (Otomatis)", "Transfer Bank Manual", "KeepIn Wallet"], horizontal=True)

                with col_det_right:
                    st.markdown("#### 📊 Ringkasan Biaya")
                    
                    # Kalkulasi live harga
                    total_harga = durasi * st.session_state["temp_harga"]
                    
                    # Komponen Ringkasan HTML bergaya Figma Premium
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-row"><span>Lokasi</span><strong>{st.session_state['temp_lokasi']}</strong></div>
                            <div class="summary-row"><span>ID Loker</span><strong>{st.session_state['temp_id_loker']}</strong></div>
                            <div class="summary-row"><span>Tipe / Ukuran</span><strong>{st.session_state['temp_tipe']}</strong></div>
                            <div class="summary-row"><span>Harga Satuan</span><strong>Rp {st.session_state['temp_harga']:,.0f} / Hari</strong></div>
                            <div class="summary-row"><span>Durasi Kontrak</span><strong>{durasi} Hari</strong></div>
                            <div class="summary-row"><span>Metode</span><strong>{metode_bayar}</strong></div>
                            <div class="summary-total"><span>Total Tagihan</span><span>Rp {total_harga:,.0f}</span></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    
                    # TOMBOL UTAMA SUBMIT KE BACKEND BOOKING_SERVICE (PORT 8001)
                    if st.button("Konfirmasi & Bayar Sekarang 🚀", type="primary", use_container_width=True):
                        # Mempersiapkan Payload Data sesuai Validasi Pydantic booking_service.py
                        payload_booking = {
                            "id_user": int(st.session_state["id_user"]),
                            "id_loker": str(st.session_state["temp_id_loker"]),
                            "nama_tempat": str(st.session_state["temp_lokasi"]),
                            "durasi_sewa": int(durasi),
                            "total_biaya": float(total_harga)
                        }
                        
                        try:
                            # Tembak API POST ke booking_service.py
                            res = requests.post(f"{BOOKING_SERVICE_URL}/create", json=payload_booking)
                            
                            if res.status_code == 201:
                                data_res = res.json()
                                st.success(f"🎉 {data_res['message']} (ID Transaksi: #{data_res['booking_id']})")
                                st.balloons()
                                
                                # Reset data langkah penampung
                                st.session_state["booking_step"] = 1
                                
                                # Otomatis alihkan halaman ke menu riwayat booking agar penyewa bisa memantau
                                st.session_state["active_menu"] = "Riwayat Booking"
                                st.rerun()
                            else:
                                st.error(f"❌ Gagal memproses data booking: {res.json().get('detail')}")
                        except Exception as e:
                            st.error("❌ Gagal terhubung ke server backend `booking_service.py` di Port 8001. Pastikan service sudah dinyalakan!")

        # ==================== KONTEN MENU RIWAYAT BOOKING ====================
        elif menu_aktif == "Riwayat Booking":
            st.subheader("📜 Riwayat Penggunaan Loker Anda")
            
            try:
                # Ambil data real-time dari booking_db lewat REST API booking_service
                res = requests.get(f"{BOOKING_SERVICE_URL}/user/{st.session_state['id_user']}")
                if res.status_code == 200:
                    daftar_booking = res.json()["data"]
                    
                    if not daftar_booking:
                        st.info("Belum ada transaksi pemesanan loker.")
                    else:
                        # Tampilkan daftar riwayat pemesanan dalam bentuk komponen kartu ekspander yang rapi
                        for b in daftar_booking:
                            with st.expander(f"📦 Order ID #{b['id_booking']} - {b['nama_tempat']} ({b['status_booking']})"):
                                st.write(f"- **Unit Loker:** {b['id_loker']}")
                                st.write(f"- **Tanggal Transaksi:** {b['tgl_booking']}")
                                st.write(f"- **Durasi Sewa:** {b['durasi_sewa']} Hari")
                                st.markdown(f"- **Total Bayar:** <span style='color:#52D1A2; font-weight:bold;'>Rp {b['total_biaya']:,.0f}</span>", unsafe_allow_html=True)
                else:
                    st.error("❌ Gagal menarik data riwayat booking.")
            except Exception as e:
                st.error("❌ Tidak bisa memuat riwayat. Pastikan backend `booking_service.py` (Port 8001) berjalan.")
                
        elif menu_aktif == "Notifikasi":
            st.subheader("🔔 Pemberitahuan Terbaru")
            st.success("🟢 Akun Anda telah berhasil dikonfirmasi dan aktif di sistem KeepIn.")
            
        elif menu_aktif == "Info Promo":
            st.subheader("🎁 Voucher Promosi Menarik Untuk Anda")
            st.metric(label="Diskon Akhir Pekan", value="30% OFF", delta="Voucher: KEEPINBARU")

    # ---------------- KONTEN KHUSUS: ROLE MITRA ----------------
    elif role_aktif.lower() == "mitra":
        st.title(f"🏢 Panel Dashboard {role_aktif} — {menu_aktif}")
        
        if menu_aktif == "Beranda":
            st.markdown("### Selamat datang kembali, Owner Mitra Bisnis! 📈")
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total Loker Dimiliki", "48 Unit", "+12% Bulan Ini")
            col_m2.metric("Loker Aktif Disewa", "36 Unit", "Sangat Produktif")
            col_m3.metric("Total Akumulasi Transaksi", "128 Transaksi", "Grafik Naik")
            
        elif menu_aktif == "Pendaftaran Usaha":
            st.subheader("➕ Daftarkan Titik Lokasi Usaha Loker Baru")
            st.text_input("Nama Tempat / Usaha Loker")
            st.text_area("Alamat Lengkap Unit")
            st.number_input("Jumlah Slot Loker yang Disediakan", min_value=1)
            st.button("Ajukan Verifikasi Lokasi")
            
        elif menu_aktif == "Laporan Bisnis":
            st.subheader("📊 Analisis Keuangan & Omset Pendapatan")
            st.write("Grafik laporan laba-rugi bisnis loker Anda akan dikalkulasikan di sini.")
            
        elif menu_aktif == "Aktivitas Loker":
            st.subheader("🔍 Monitoring Real-Time Penggunaan Unit Loker")
            st.markdown("🟢 **Unit A-01:** Sedang digunakan oleh Budi Santoso (Sisa Waktu: 2 Jam)")
            st.markdown("⚪ **Unit A-02:** Tersedia (Kosong)")
            
        elif menu_aktif == "Penarikan Saldo":
            st.subheader("💳 Tarik Pendapatan Bisnis Loker")
            st.metric("Saldo Siap Cair", "Rp 4.520.000")
            st.button("Tarik Dana ke Rekening Utama")