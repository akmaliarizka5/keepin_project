import streamlit as st

from views.booking_history_page import render_booking_history_page
from views.booking_page import render_booking_page
from views.mitra_page import render_mitra_page


def render_dashboard_page(logo_html):
    role_aktif = st.session_state["user_role"]
    email_user = st.session_state["user_email"]
    first_name = email_user.split("@")[0].split(".")[0].title() if email_user else "User"
    initials = "".join(part[:1] for part in first_name.split()[:2]).upper() or "U"
    try:
        if st.query_params.get("menu") == "profile":
            st.session_state["active_menu"] = "Profil Saya"
            st.query_params.clear()
    except Exception:
        pass

    with st.sidebar:
        st.markdown(
            f"""
            <div class="k-sidebar-brand">
                <div class="k-sidebar-logo">{logo_html}</div>
                <div>
                    <div class="k-sidebar-title">KeepIn</div>
                    <div class="k-sidebar-caption">Smart locker console</div>
                </div>
                <span class="k-role-pill">{role_aktif}</span>
            </div>
            <div class="k-sidebar-user">
                <div class="k-avatar-sm">{initials}</div>
                <div class="k-sidebar-user-copy">
                    <b>{first_name}</b>
                    <span>{email_user}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if role_aktif.lower() == "penyewa":
            list_menu = ["Beranda", "Booking", "Riwayat Booking", "Notifikasi", "Info Promo"]
        elif role_aktif.lower() == "mitra":
            list_menu = ["Beranda", "Pendaftaran Usaha", "Laporan Bisnis", "Aktivitas Loker", "Penarikan Saldo"]
        else:
            list_menu = ["Beranda", "Manajemen User", "Sistem Server"]

        hidden_menu = ["Profil Saya"]
        if st.session_state["active_menu"] not in list_menu + hidden_menu:
            st.session_state["active_menu"] = list_menu[0]

        st.markdown('<div class="k-section-label">Menu</div>', unsafe_allow_html=True)
        for menu in list_menu:
            icon = get_menu_icon(menu)
            if menu == st.session_state["active_menu"]:
                st.markdown(f'<div class="k-nav-active"><span>{icon}</span><b>{menu}</b></div>', unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {menu}", key=f"nav_{menu}"):
                    st.session_state["active_menu"] = menu
                    try:
                        st.query_params.clear()
                    except Exception:
                        pass
                    st.rerun()

        st.markdown('<div class="k-sidebar-spacer"></div>', unsafe_allow_html=True)
        if st.button("Keluar", key="logout_btn", help="Keluar dari akun"):
            st.session_state["current_page"] = "login"
            st.session_state["user_role"] = None
            st.session_state["user_email"] = None
            st.session_state["id_user"] = None
            st.session_state["active_menu"] = "Beranda"
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.rerun()

    render_topbar(first_name, role_aktif, email_user, initials)
    menu_aktif = st.session_state["active_menu"]

    if menu_aktif == "Profil Saya":
        render_profile_page(first_name, email_user, role_aktif, initials)
    elif role_aktif.lower() == "penyewa":
        render_penyewa_page(first_name, menu_aktif)
    elif role_aktif.lower() == "mitra":
        render_mitra_page(role_aktif, menu_aktif)
    else:
        render_admin_page(menu_aktif)


def get_menu_icon(menu):
    icons = {
        "Beranda": "H",
        "Booking": "B",
        "Riwayat Booking": "R",
        "Notifikasi": "N",
        "Info Promo": "%",
        "Pendaftaran Usaha": "+",
        "Laporan Bisnis": "L",
        "Aktivitas Loker": "A",
        "Penarikan Saldo": "P",
        "Manajemen User": "U",
        "Sistem Server": "S",
    }
    return icons.get(menu, "-")


def render_topbar(first_name, role, email, initials):
    st.markdown(
        f"""
        <div class="k-topbar">
            <div></div>
            <a class="k-profile-preview" href="?menu=profile" title="Buka profil {email}">
                <div class="k-user-mini">Hai, {first_name}<br><span>{role.upper()}</span></div>
                <div class="k-avatar">{initials}</div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_penyewa_page(first_name, menu_aktif):
    if menu_aktif == "Beranda":
        render_penyewa_home(first_name)
    elif menu_aktif == "Booking":
        render_booking_page()
    elif menu_aktif == "Riwayat Booking":
        render_booking_history_page()
    elif menu_aktif == "Notifikasi":
        render_notifications()
    elif menu_aktif == "Info Promo":
        render_promos()


def render_profile_page(first_name, email, role, initials):
    st.markdown(
        f"""
        <div class="k-profile-hero">
            <div class="k-profile-cover"></div>
            <div class="k-profile-main">
                <div class="k-avatar-xl">{initials}</div>
                <div>
                    <span class="k-chip k-chip-green">{role}</span>
                    <h1>{first_name}</h1>
                    <p>{email}</p>
                </div>
            </div>
        </div>
        <div class="k-dashboard-grid">
            <div class="k-card">
                <div class="k-section-label" style="margin-top:0;">Informasi Akun</div>
                <div class="k-mini-row"><span>Nama tampilan</span><strong>{first_name}</strong></div>
                <div class="k-mini-row"><span>Email</span><strong>{email}</strong></div>
                <div class="k-mini-row"><span>Role aktif</span><strong>{role}</strong></div>
                <div class="k-mini-row"><span>Status akun</span><span class="k-chip k-chip-green">Aktif</span></div>
            </div>
            <div class="k-card">
                <div class="k-section-label" style="margin-top:0;">Keamanan</div>
                <div class="k-mini-row"><span>Session</span><span class="k-chip">Terhubung</span></div>
                <div class="k-mini-row"><span>Database user</span><span class="k-chip k-chip-green">Ready</span></div>
                <p class="k-muted" style="margin-top:16px;">Profil ini memakai data login dan session state aplikasi. Edit profil penuh bisa ditambahkan sebagai modul berikutnya.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_penyewa_home(first_name):
    st.markdown(
        f"""
        <div class="k-hero-grid">
            <div class="k-shell">
                <span class="k-chip k-chip-green">Yogyakarta live coverage</span>
                <h1>Simpan barang tanpa drama.</h1>
                <p>Hai {first_name}, cari loker terdekat, lihat titiknya di map, pilih ukuran, lalu bayar dalam satu alur yang rapi.</p>
                <div style="display:flex;gap:12px;margin-top:28px;">
                    <span class="k-chip k-chip-green">9 lokasi ready</span>
                    <span class="k-chip">Mulai Rp 8.000/jam</span>
                    <span class="k-chip k-chip-purple">Payment simulasi aktif</span>
                </div>
            </div>
            <div class="k-glass" style="background:#FFFFFF;color:#162235;border-color:#E7ECF3;box-shadow:0 20px 70px rgba(17,24,39,.08);">
                <div class="k-section-label" style="margin-top:0;">Hari Ini</div>
                <div class="k-mini-row"><span>Loker tersedia</span><strong>9</strong></div>
                <div class="k-mini-row"><span>Area aktif</span><strong>Yogyakarta</strong></div>
                <div class="k-mini-row"><span>Promo aktif</span><strong>30% OFF</strong></div>
                <div class="k-mini-row"><span>Status layanan</span><span class="k-chip k-chip-green">Online</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="k-section-label">Akses Cepat</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="k-action-grid">
            <div class="k-action-card"><div class="k-icon">01</div><h3>Booking Loker</h3><p class="k-muted">Cari lokasi, bandingkan harga, dan pesan unit dalam hitungan detik.</p></div>
            <div class="k-action-card"><div class="k-icon" style="background:#EEF2FF;color:#4F46E5;">02</div><h3>Riwayat & Payment</h3><p class="k-muted">Pantau status booking dan tandai payment simulasi tanpa pindah halaman.</p></div>
            <div class="k-action-card"><div class="k-icon" style="background:#FFF7ED;color:#F97316;">03</div><h3>Promo Aktif</h3><p class="k-muted">Gunakan kode promo untuk menghemat biaya penyimpanan.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    left, right = st.columns([1.1, .9])
    with left:
        st.markdown(
            """
            <div class="k-card">
                <div class="k-section-label" style="margin-top:0;">Booking Terakhir</div>
                <div class="k-mini-row"><div><b>Malioboro Mall</b><br><span class="k-muted">MALIO-A01 - 3 jam</span></div><span class="k-chip k-chip-green">PAID</span></div>
                <div class="k-mini-row"><div><b>Ambarrukmo Plaza</b><br><span class="k-muted">AMPLAZ-B01 - 2 jam</span></div><span class="k-chip">PENDING</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="k-orb-card">
                <span class="k-chip k-chip-green">Weekend Deal</span>
                <h2 style="font-size:44px;margin:18px 0 4px;">30% OFF</h2>
                <p class="k-muted">Kode KEEPINBARU aktif untuk booking pertama di area Jogja.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_notifications():
    st.markdown('<div class="welcome-title">Notifikasi</div>', unsafe_allow_html=True)
    st.markdown('<span class="k-role-pill">3 pesan baru</span>', unsafe_allow_html=True)
    notifications = [
        ("Booking Berhasil Dikonfirmasi", "Booking Anda di Loker Central Point JKT telah dikonfirmasi."),
        ("Pembayaran Diterima", "Pembayaran sebesar Rp 25.000 berhasil diverifikasi."),
        ("Promo Terbatas", "Dapatkan diskon 20% untuk semua unit Large."),
        ("Waktu Sewa Segera Berakhir", "Sisa waktu sewa Anda tinggal 30 menit."),
    ]
    for title, body in notifications:
        st.markdown(f'<div class="k-card-soft" style="margin-bottom:12px;border-left:4px solid #52C7AF;"><b>{title}</b><br><span class="k-muted">{body}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="k-hero-dark"><h2>Push Notifications</h2><p>Aktifkan notifikasi untuk status booking dan promo terbaru.</p></div>', unsafe_allow_html=True)


def render_promos():
    st.markdown(
        """
        <div class="k-hero-dark" style="max-width:760px;margin:auto;">
            <span class="k-chip k-chip-green">HOT DEAL ALERT</span>
            <h2>Flash Sale<br>Weekend Surprise!</h2>
            <p>Potongan harga flat untuk semua booking di bandara dan mall.</p>
            <span class="k-chip">SURPRISE15</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="k-section-label" style="max-width:760px;margin-left:auto;margin-right:auto;">Available Offers</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="k-card"><span class="k-chip k-chip-green">Eksklusif</span><h2>30% OFF</h2><b>Diskon Booking Pertama</b><p class="k-muted">Khusus pengguna baru KeepIn.</p><span class="k-chip">KEEPINBARU</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="k-card"><span class="k-chip k-chip-green">Event</span><h2>Rp 10rb OFF</h2><b>Promo Stasiun KRL</b><p class="k-muted">Potongan untuk area stasiun dan kampus.</p><span class="k-chip">KERETAASIK</span></div>', unsafe_allow_html=True)


def render_admin_page(menu_aktif):
    st.title(f"Admin - {menu_aktif}")
    st.info("Panel admin disiapkan sebagai placeholder untuk monitoring user dan status service.")
