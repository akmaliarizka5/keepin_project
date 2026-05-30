import requests
import streamlit as st

from services.auth_client import parse_response, register


def render_register_page():
    col_reg_left, col_reg_space, col_reg_right = st.columns([1.2, 0.1, 1.3])

    with col_reg_left:
        st.markdown("""
            <div style="background-color:#1E293B; padding:40px; border-radius:8px; color:white; min-height:550px;">
                <h2 style='color:white; font-weight:800;'>Mulai gunakan KeepIn.</h2>
                <p style='color:#94A3B8; font-size:14px;'>Buat akun sebagai penyewa untuk booking loker, atau sebagai mitra untuk mendaftarkan titik usaha.</p>
                <br><br>
                <div style='margin-bottom:20px;'><b>Data siap integrasi</b><br><small style='color:#94A3B8;'>Auth, loker, booking, payment, dan usaha sudah terpisah per service.</small></div>
                <div style='margin-bottom:20px;'><b>Flow end-to-end</b><br><small style='color:#94A3B8;'>Dari pencarian loker sampai payment simulasi.</small></div>
                <div><b>Demo lokal</b><br><small style='color:#94A3B8;'>Seed data tersedia untuk area Yogyakarta.</small></div>
            </div>
        """, unsafe_allow_html=True)

    with col_reg_right:
        if st.button("Kembali ke Login", key="back_to_login_top"):
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

        if st.button("Daftar Akun", type="primary"):
            if not nama_lengkap or not reg_email or not reg_password:
                st.warning("Harap lengkapi semua kolom pendaftaran yang wajib.")
            else:
                payload = {
                    "nama_lengkap": nama_lengkap,
                    "email": reg_email,
                    "no_telp": reg_telp if reg_telp else "-",
                    "password": reg_password,
                    "role": reg_role,
                }
                try:
                    response = register(payload)
                    res_data, error_msg = parse_response(response)

                    if response.status_code == 201 and res_data:
                        st.success(res_data["message"])
                        st.info("Silakan kembali ke Login untuk mencoba akun baru Anda.")
                    else:
                        st.error(f"Registrasi gagal: {error_msg}")
                except requests.exceptions.ConnectionError:
                    st.error("Gagal terhubung ke auth_service.py.")
