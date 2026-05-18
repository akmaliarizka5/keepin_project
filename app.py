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
            
        # ==================== KONTEN MENU BOOKING ====================
        elif menu_aktif == "Booking":
            st.subheader("📍 Cari dan Pesan Loker Strategis")
            
            st.markdown("### Daftar Loker Tersedia di **Kuningan City Mall**")
            
            # Membuat grid layout untuk pilihan unit loker
            col_l1, col_l2, col_l3 = st.columns(3)
            
            with col_l1:
                st.info("📦 **Unit: LK-01**\nTipe: Standard (S)\nHarga: Rp 20.000 / Hari")
                book_lk01 = st.button("Pilih & Sewa LK-01")
            with col_l2:
                st.info("📦 **Unit: LK-02**\nTipe: Medium (M)\nHarga: Rp 35.000 / Hari")
                book_lk02 = st.button("Pilih & Sewa LK-02")
            with col_l3:
                st.info("📦 **Unit: LK-03**\nTipe: Large (L)\nHarga: Rp 50.000 / Hari")
                book_lk03 = st.button("Pilih & Sewa LK-03")
                
            # Logika penentuan klik tombol unit
            if book_lk01 or book_lk02 or book_lk03:
                id_terpilih = "LK-01" if book_lk01 else ("LK-02" if book_lk02 else "LK-03")
                harga_terpilih = 20000.0 if book_lk01 else (35000.0 if book_lk02 else 50000.0)
                
                # PERBAIKAN TYPO: Simpan bersih langsung ke session state tanpa 'id_terpiled'
                st.session_state["temp_id_loker"] = id_terpilih
                st.session_state["temp_harga"] = harga_terpilih
                st.session_state["show_form_konfirmasi"] = True

            # Tampilkan formulir durasi sewa jika salah satu unit loker di klik
            if st.session_state.get("show_form_konfirmasi"):
                st.markdown("---")
                st.write(f"### 📝 Formulir Konfirmasi Sewa Unit **{st.session_state['temp_id_loker']}**")
                
                durasi = st.number_input("Durasi Sewa (Hari)", min_value=1, max_value=30, value=1)
                total_harga = durasi * st.session_state["temp_harga"]
                
                st.write(f"**Total Biaya Layanan Sewa:** Rp {total_harga:,.0f}")
                
                if st.button("Konfirmasi & Buat Pesanan", type="primary"):
                    payload_booking = {
                        "id_user": st.session_state["id_user"],
                        "id_loker": st.session_state["temp_id_loker"],
                        "nama_tempat": "Kuningan City Mall",
                        "durasi_sewa": durasi,
                        "total_biaya": total_harga
                    }
                    
                    try:
                        # Menembak ke booking_service.py di port 8001
                        res = requests.post(f"{BOOKING_SERVICE_URL}/create", json=payload_booking)
                        if res.status_code == 201:
                            st.success(f"🎉 {res.json()['message']} ID Booking: {res.json()['booking_id']}")
                            st.balloons()
                            st.session_state["show_form_konfirmasi"] = False
                            
                            # Otomatis alihkan halaman ke menu riwayat booking
                            st.session_state["active_menu"] = "Riwayat Booking"
                            st.rerun()
                        else:
                            st.error(f"❌ Gagal melakukan booking: {res.json().get('detail')}")
                    except Exception as e:
                        st.error("❌ Gagal terhubung ke `booking_service.py`. Pastikan service port 8001 sudah aktif!")

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