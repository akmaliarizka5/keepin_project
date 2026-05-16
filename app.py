# app.py
from PIL import Image
import streamlit as st
import requests
from io import BytesIO
import base64

# URL Endpoint Microservice Auth
AUTH_SERVICE_URL = "http://127.0.0.1:8000/api/auth/login"

icon_img = Image.open("./src/images/icon.png")
st.set_page_config(
    page_title="KeepIn - Masuk ke Akun",
    page_icon=icon_img,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
    div.row-widget.stButton > button { width: 100%; background-color: #1E293B; color: white; font-weight: 600; padding: 12px; border-radius: 8px; border: none; margin-top: 20px; }
    div.row-widget.stButton > button:hover { background-color: #0F172A; color: white; }
    
    .register-text {
        text-align: center;
        font-size: 14px;
        color: #64748B;
        margin-top: 15px;
    }
    .register-link {
        color: #52D1A2;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

col_left, col_space, col_right = st.columns([1.2, 0.2, 1.2])

# ==================== SISI KIRI: LOGIN FORM ====================
with col_left:
    def image_to_base64(img):
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    
    try:
        logo_img = Image.open("./src/images/logo.png")
        logo_base64 = image_to_base64(logo_img)
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="30">'
    except FileNotFoundError:
        logo_html = '🟢'

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">
            {logo_html}
            <span style="font-size:24px; font-weight:bold; color:#1E293B;">KeepIn</span>
            <span style="font-size:12px; background-color:#E6F9F2; color:#52D1A2; padding:3px 8px; border-radius:5px; font-weight:bold;">
                Mitra
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="welcome-title">Selamat datang kembali! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Masuk ke akun Anda untuk mengelola loker, memantau pendapatan, dan meningkatkan performa bisnis.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-label">Pilih Role Anda</div>', unsafe_allow_html=True)
    selected_role_idx = st.radio("Role", ["Mitra", "Penyewa", "Admin"], horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="Masukkan email Anda", label_visibility="collapsed")
    
    st.markdown('<div class="form-label">Kata Sandi</div>', unsafe_allow_html=True)
    password = st.text_input("Kata Sandi", type="password", placeholder="Masukkan kata sandi", label_visibility="collapsed")
    
    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        ingat_saya = st.checkbox("Ingat saya")
    with col_p2:
        st.markdown("<p style='text-align: right; margin-top: 4px;'><a href='#' style='color:#52D1A2; font-size:14px; text-decoration:none; font-weight:600;'>Lupa kata sandi?</a></p>", unsafe_allow_html=True)
        
    if st.button("Masuk ke Akun"):
        if not email or not password:
            st.warning("Harap isi Email dan Kata Sandi terlebih dahulu!")
        else:
            payload = {
                "email": email,
                "password": password,
                "role": selected_role_idx
            }
            
            try:
                response = requests.post(AUTH_SERVICE_URL, json=payload)
                
                # PERBAIKAN AMAN: Cek apakah response berupa JSON valid sebelum diekstrak
                try:
                    res_data = response.json()
                except ValueError:
                    res_data = None

                if response.status_code == 200 and res_data:
                    st.success(f"🎉 {res_data['message']} sebagai {res_data['user']['role']}!")
                    st.session_state["token"] = res_data["token"]
                    st.session_state["user_email"] = res_data["user"]["email"]
                else:
                    error_msg = res_data.get('detail', 'Terjadi kesalahan internal') if res_data else response.text
                    st.error(f"❌ Login Gagal: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Gagal terhubung ke `auth_service.py`. Pastikan backend service sudah dinyalakan!")

    st.markdown(
        """
        <div class="register-text">
            Belum punya akun? <a class="register-link" href="#">Daftar sekarang</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<p style='text-align: center; color:#64748B; font-size:12px; font-weight:600; margin-top:30px;'>ATAU MASUK DENGAN</p>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([1, 1])
    with col_g1: st.button("🌐 Google", key="btn_google")
    with col_g2: st.button("🍏 Apple", key="btn_apple")


# ==================== SISI KANAN ====================
with col_right:
    st.write("##")
    st.write("##")
    st.markdown('<div class="right-title">Satu platform untuk <br><span class="highlight-text">semua kebutuhan loker.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="right-subtitle">Baik Anda mitra, penyewa, atau admin. KeepIn siap membantu.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-box"><div class="feature-icon-1">🟢</div><div><div class="feature-title">Kelola Bisnis Lebih Mudah</div><div class="feature-desc">Pantau pendapatan, booking, dan performa loker secara real-time.</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><div class="feature-icon-2">🔵</div><div><div class="feature-title">Booking Cepat & Praktis</div><div class="feature-desc">Cari loker terdekat dan booking dalam hitungan detik.</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box"><div class="feature-icon-3">🟠</div><div><div class="feature-title">Sistem Aman & Terpercaya</div><div class="feature-desc">Data Anda terlindungi dengan enkripsi berstandar tinggi.</div></div></div>', unsafe_allow_html=True)