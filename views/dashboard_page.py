import streamlit as st

from views.booking_history_page import render_booking_history_page
from views.booking_page import render_booking_page
from views.mitra_page import render_mitra_page


def render_dashboard_page(logo_html):
    role_aktif = st.session_state["user_role"]
    email_user = st.session_state["user_email"]

    with st.sidebar:
        st.markdown(f'<div style="display:flex; align-items:center; gap:10px; margin-bottom: 25px;">{logo_html}<span style="font-size:22px; font-weight:bold; color:#1E293B;">KeepIn <small style="font-size:10px; background:#EEF2FF; color:#4F46E5; padding:2px 6px; border-radius:4px;">{role_aktif.upper()}</small></span></div>', unsafe_allow_html=True)
        st.write(f"📧 `{email_user}`")
        st.write("---")
        
        if role_aktif.lower() == "penyewa":
            list_menu = ["Beranda", "Booking", "Riwayat Booking", "Notifikasi", "Info Promo"]
        elif role_aktif.lower() == "mitra":
            list_menu = ["Beranda", "Pendaftaran Usaha", "Laporan Bisnis", "Aktivitas Loker", "Penarikan Saldo"]
        else:
            list_menu = ["Beranda", "Manajemen User", "Sistem Server"]
            
        if st.session_state["active_menu"] not in list_menu:
            st.session_state["active_menu"] = list_menu[0]

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

    menu_aktif = st.session_state["active_menu"]
    
    if role_aktif.lower() == "penyewa":
        render_penyewa_page(role_aktif, menu_aktif)
    elif role_aktif.lower() == "mitra":
        render_mitra_page(role_aktif, menu_aktif)


def render_penyewa_page(role_aktif, menu_aktif):
    st.title(f"💼 Portal {role_aktif} — {menu_aktif}")
    
    if menu_aktif == "Beranda":
        st.markdown(f"### Selamat datang kembali, {st.session_state['user_email']}! 👋")
        st.info("💡 Pilih menu **Booking** di sidebar kiri Anda untuk mulai mencari dan menyewa loker terdekat.")
        
    elif menu_aktif == "Booking":
        render_booking_page()

    elif menu_aktif == "Riwayat Booking":
        render_booking_history_page()
            
    elif menu_aktif == "Notifikasi":
        st.subheader("🔔 Pemberitahuan Terbaru")
        st.success("🟢 Akun Anda telah berhasil dikonfirmasi dan aktif di sistem KeepIn.")
        
    elif menu_aktif == "Info Promo":
        st.subheader("🎁 Voucher Promosi Menarik Untuk Anda")
        st.metric(label="Diskon Akhir Pekan", value="30% OFF", delta="Voucher: KEEPINBARU")
