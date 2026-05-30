import requests
import streamlit as st

from services.auth_client import login


def render_login_page(logo_html):
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
        with col_p1:
            st.checkbox("Ingat saya")
        with col_p2:
            st.markdown("<p style='text-align: right; margin-top: 4px;'><a href='#' style='color:#52D1A2; font-size:14px; text-decoration:none; font-weight:600;'>Lupa kata sandi?</a></p>", unsafe_allow_html=True)
            
        st.markdown('<div class="login-btn-container">', unsafe_allow_html=True)
        if st.button("Masuk ke Akun"):
            if not email or not password:
                st.warning("Harap isi Email dan Kata Sandi terlebih dahulu!")
            else:
                payload = {"email": email, "password": password, "role": selected_role}
                try:
                    response = login(payload)
                    res_data = response.json() if response.headers.get('content-type') == 'application/json' else None
                    
                    if response.status_code == 200 and res_data:
                        st.session_state["token"] = res_data["token"]
                        st.session_state["user_email"] = res_data["user"]["email"]
                        st.session_state["user_role"] = res_data["user"]["role"]
                        st.session_state["id_user"] = res_data["user"]["id_user"]
                        st.session_state["current_page"] = "dashboard"
                        st.session_state["active_menu"] = "Beranda"
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
