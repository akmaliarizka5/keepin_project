import streamlit as st
import requests

# Mengeset layout agar memenuhi layar (Wide mode) seperti pada UI/UX temanmu
st.set_page_config(page_title="Keepin Console", layout="wide", initial_sidebar_state="expanded")

BACKEND_URL = "http://127.0.0.1:8000"

# Inisialisasi Session State agar aplikasi mengingat status login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user_role = None
    st.session_state.user_nama = None
    st.session_state.page = "Login"

# --- FUNGSI LOGOUT ---
def logout():
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user_role = None
    st.session_state.user_nama = None
    st.session_state.page = "Login"
    st.rerun()

# ==============================================================================
# VIEW 1: SEBELUM LOGIN (LOGIN & REGISTER PAGE)
# ==============================================================================
if not st.session_state.authenticated:
    
    # Navigasi kecil perpindahan Login <-> Register
    sub_tab = st.radio("Navigasi", ["Masuk Akun", "Daftar Akun Baru"], horizontal=True, label_visibility="collapsed")
    
    if sub_tab == "Daftar Akun Baru":
        st.title("📦 Keepin Console - Daftar Akun Baru")
        role = st.selectbox("Daftar Sebagai", ["Penyewa", "Mitra"])
        nama_lengkap = st.text_input("Nama Lengkap", placeholder="Contoh: Andi Pratama")
        email = st.text_input("Email", placeholder="nama@email.com")
        no_telp = st.text_input("No. Telp", placeholder="081234567XXX")
        password = st.text_input("Kata Sandi (Minimal 8 Karakter)", type="password")
        
        if st.button("Daftar Akun", type="primary"):
            payload = {
                "nama_lengkap": nama_lengkap,
                "email": email,
                "no_telp": no_telp,
                "password": password,
                "role": role
            }
            res = requests.post(f"{BACKEND_URL}/api/auth/register", json=payload)
            if res.status_code == 201:
                st.success(res.json()["message"])
                st.info("Silakan beralih ke menu 'Masuk Akun'.")
            else:
                st.error(f"Gagal mendaftar: {res.json().get('detail')}")
                
    elif sub_tab == "Masuk Akun":
        st.title("👋 Selamat datang kembali di Keepin!")
        email = st.text_input("Email")
        password = st.text_input("Kata Sandi", type="password")
        
        if st.button("Masuk ke Akun", type="primary"):
            payload = {"email": email, "password": password}
            res = requests.post(f"{BACKEND_URL}/api/auth/login", json=payload)
            
            if res.status_code == 200:
                data = res.json()
                st.session_state.authenticated = True
                st.session_state.token = data["access_token"]
                st.session_state.user_role = data["role"]
                st.session_state.user_nama = data["nama"]
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error(f"Gagal masuk: {res.json().get('detail')}")

# ==============================================================================
# VIEW 2: SETELAH LOGIN (DASHBOARD PENYEWA ATAU MITRA)
# ==============================================================================
else:
    # Membuat Sidebar Navigasi seperti struktur di UI/UX kamu
    st.sidebar.title("Keepin App")
    st.sidebar.write(f"Logged in as: **{st.session_state.user_nama}** ({st.session_state.user_role})")
    
    if st.session_state.user_role == "Penyewa":
        menu = st.sidebar.radio("Menu Penyewa", ["Beranda", "Booking", "Riwayat Booking", "Notifikasi", "Info Promo"])
        st.sidebar.button("Keluar", on_click=logout)
        
        if menu == "Beranda":
            st.header(f"Selamat datang kembali, {st.session_state.user_nama}! 👋")
            st.caption("Temukan loker terdekat dan simpan barangmu dengan aman.")
            st.text_input("🔍 Cari lokasi, tempat, atau area...")
            # Komponen visual banner diskon dsb diletakkan di sini...
            
        elif menu == "Booking":
            st.header("📍 Cari Loker Terdekat")
            # [NEXT DEVELOPMENT COMMENT]:
            # Di sini Streamlit harus melakukan requests.get() ke `loker_service` untuk mengambil list master loker
            # Contoh: headers = {"Authorization": f"Bearer {st.session_state.token}"}
            # res = requests.get("http://api-gateway/api/lockers/available", headers=headers)
            st.info("Fitur maps dan pemilihan unit loker akan tersambung ke `loker_service`.")
            
        elif menu == "Riwayat Booking":
            st.header("📄 Riwayat Pesanan Anda")
            # [NEXT DEVELOPMENT COMMENT]: Mengambil log pesanan dari `booking_service` berdasarkan user_id di token.
            st.write("Belum ada pesanan aktif.")

    elif st.session_state.user_role == "Mitra":
        menu = st.sidebar.radio("Menu Partner/Mitra", ["Beranda", "Pendaftaran Usaha", "Laporan Bisnis", "Aktivitas Loker", "Tarik Saldo"])
        st.sidebar.button("Keluar", on_click=logout)
        
        if menu == "Beranda":
            st.header("Selamat datang kembali, Mitra! 💼")
            # [NEXT DEVELOPMENT COMMENT]: Menampilkan total ringkasan dari `usaha_service` dan `booking_service`
            st.metric(label="Total Loker Dimiliki", value="48 Unit")
            st.metric(label="Loker Aktif Tersewa", value="36 Unit")
            
        elif menu == "Pendaftaran Usaha":
            st.header("🏢 Daftarkan Usaha/Cabang Loker Baru")
            nama_usaha = st.text_input("Nama Usaha Loker")
            alamat_usaha = st.text_area("Alamat Lengkap Cabang")
            jenis = st.selectbox("Jenis Loker", ["Standard", "Digital/Automated", "Kombinasi"])
            
            if st.button("Ajukan Kemitraan Usaha", type="primary"):
                # [NEXT DEVELOPMENT COMMENT]: 
                # Kirim data form ini ke `usaha_service` dengan menyertakan Token JWT Mitra di header.
                # Data disimpan ke dalam `usaha_db` pada tabel usaha (terdapat kolom mitra_id).
                st.success("Formulir terkirim! Menunggu validasi sistem utama.")