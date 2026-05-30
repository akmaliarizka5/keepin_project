import requests
import streamlit as st

from services.auth_client import login, parse_response


def render_login_page(logo_html):
    col_left, col_space, col_right = st.columns([1.2, 0.2, 1.2])

    with col_left:
        st.markdown(f'<div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">{logo_html}<span style="font-size:24px; font-weight:bold; color:#1E293B;">KeepIn</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Selamat datang kembali</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Masuk untuk mencari loker, mengelola booking, atau memantau usaha mitra.</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-label">Pilih Role Anda</div>', unsafe_allow_html=True)
        selected_role = st.radio("Role", ["Penyewa", "Mitra", "Admin"], horizontal=True, label_visibility="collapsed")

        st.markdown('<div class="form-label">Email</div>', unsafe_allow_html=True)
        email = st.text_input("Email Login", placeholder="Contoh: andi@keepin.example.com", label_visibility="collapsed")

        st.markdown('<div class="form-label">Kata Sandi</div>', unsafe_allow_html=True)
        password = st.text_input("Kata Sandi Login", type="password", placeholder="Masukkan kata sandi", label_visibility="collapsed")

        st.caption("Demo: andi@keepin.example.com / password123 atau maya@keepin.example.com / password123")

        st.markdown('<div class="login-btn-container">', unsafe_allow_html=True)
        if st.button("Masuk ke Akun"):
            if not email or not password:
                st.warning("Harap isi Email dan Kata Sandi terlebih dahulu.")
            else:
                payload = {"email": email, "password": password, "role": selected_role}
                try:
                    response = login(payload)
                    res_data, error_msg = parse_response(response)

                    if response.status_code == 200 and res_data:
                        st.session_state["token"] = res_data["token"]
                        st.session_state["user_email"] = res_data["user"]["email"]
                        st.session_state["user_role"] = res_data["user"]["role"]
                        st.session_state["id_user"] = res_data["user"]["id_user"]
                        st.session_state["current_page"] = "dashboard"
                        st.session_state["active_menu"] = "Beranda"
                        st.rerun()
                    else:
                        st.error(f"Login gagal: {error_msg}")
                except requests.exceptions.ConnectionError:
                    st.error("Gagal terhubung ke auth_service.py. Pastikan service port 8000 aktif.")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Belum punya akun? Daftar sekarang", key="go_to_register_btn"):
            st.session_state["current_page"] = "register"
            st.rerun()

    with col_right:
        st.write("##")
        st.markdown('<div class="right-title">Satu platform untuk <br><span class="highlight-text">loker digital.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="right-subtitle">Cari loker terdekat, booking per jam, bayar dengan simulasi payment, dan pantau usaha mitra dalam satu dashboard.</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-1"></div><div><div class="feature-title">Map Interaktif</div><div class="feature-desc">Titik loker muncul langsung di peta PyDeck area Jogja.</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-2"></div><div><div class="feature-title">Booking Cepat</div><div class="feature-desc">Pilih ukuran, harga, durasi jam, lalu buat payment simulasi.</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-box"><div class="feature-icon-3"></div><div><div class="feature-title">Panel Mitra</div><div class="feature-desc">Daftarkan usaha, lihat slot, dan pantau performa operasional.</div></div></div>', unsafe_allow_html=True)
