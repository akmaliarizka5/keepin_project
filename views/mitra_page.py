import streamlit as st

from services.usaha_client import create_usaha, get_usaha_by_owner, get_usaha_summary


def render_mitra_page(role_aktif, menu_aktif):
    if menu_aktif == "Beranda":
        render_mitra_home()
    elif menu_aktif == "Pendaftaran Usaha":
        render_pendaftaran_usaha()
    elif menu_aktif == "Laporan Bisnis":
        render_laporan_bisnis()
    elif menu_aktif == "Aktivitas Loker":
        render_aktivitas_loker()
    elif menu_aktif == "Penarikan Saldo":
        render_penarikan_saldo()


def get_summary():
    summary = {"total_usaha": 0, "total_loker": 0, "usaha_aktif": 0}
    try:
        res = get_usaha_summary(st.session_state["id_user"])
        if res.status_code == 200 and res.json().get("data"):
            summary = res.json()["data"]
    except Exception:
        pass
    return summary


def render_mitra_home():
    summary = get_summary()
    st.markdown('<div class="welcome-title">Selamat datang kembali, Mitra.</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Kelola usaha dan pantau performa loker Anda dengan mudah.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="k-card-soft" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;">
            <div><b style="font-size:20px;">Daftarkan Usaha Baru</b><br><span class="k-muted">Tambahkan usaha Anda untuk mulai mengelola loker.</span></div>
            <span class="k-chip k-chip-green">Daftarkan sekarang</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    render_metric_card(c1, "Total Usaha", summary.get("total_usaha", 0))
    render_metric_card(c2, "Total Loker", summary.get("total_loker", 0))
    render_metric_card(c3, "Loker Aktif", 36)
    render_metric_card(c4, "Total Booking", 128)

    st.markdown('<div class="k-section-label">Daftar Usaha Saya</div>', unsafe_allow_html=True)
    render_usaha_table()


def render_metric_card(column, label, value):
    with column:
        st.markdown(f'<div class="k-card k-stat"><div class="label">{label}</div><div class="value">{value}</div><span class="k-muted">+12% vs last month</span></div>', unsafe_allow_html=True)


def render_pendaftaran_usaha():
    st.markdown('<div class="welcome-title" style="font-size:22px;">Pendaftaran Usaha Baru</div>', unsafe_allow_html=True)
    step = st.session_state.get("mitra_register_step", 1)
    render_stepper(step)
    if step == 1:
        render_register_step_location()
    elif step == 2:
        render_register_step_unit()
    else:
        render_register_step_confirm()


def render_stepper(step):
    labels = ["Informasi Dasar", "Spesifikasi Unit", "Konfirmasi"]
    cols = st.columns(3)
    for idx, col in enumerate(cols, start=1):
        active = "#1E293B" if idx <= step else "#FFFFFF"
        color = "white" if idx <= step else "#CBD5E1"
        with col:
            st.markdown(f'<div style="text-align:center;"><span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:999px;background:{active};color:{color};font-weight:900;border:1px solid #E2E8F0;">{idx}</span><br><span class="k-muted">{labels[idx-1]}</span></div>', unsafe_allow_html=True)


def render_register_step_location():
    form = st.session_state.setdefault("mitra_usaha_form", {})
    left, center, right = st.columns([1, 1.3, 1])
    with center:
        st.markdown('<div class="k-card"><h3>Detail Lokasi Bisnis</h3><span class="k-muted">Lengkapi informasi alamat dimana unit loker akan ditempatkan.</span>', unsafe_allow_html=True)
        form["nama_usaha"] = st.text_input("Nama Usaha / Lokasi", value=form.get("nama_usaha", ""), placeholder="Contoh: Kopi Kita Malioboro")
        form["alamat"] = st.text_area("Alamat Lengkap", value=form.get("alamat", ""), placeholder="Jl. Malioboro No. 123, Yogyakarta")
        st.map([{"lat": -7.7956, "lon": 110.3695}], zoom=12)
        c1, c2 = st.columns(2)
        form["latitude"] = c1.text_input("Latitude", value=form.get("latitude", "-7.7956"))
        form["longitude"] = c2.text_input("Longitude", value=form.get("longitude", "110.3695"))
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Lanjut Tahapan"):
            st.session_state["mitra_register_step"] = 2
            st.rerun()


def render_register_step_unit():
    form = st.session_state.setdefault("mitra_usaha_form", {})
    st.markdown('<div style="text-align:center;"><h2>Pilih Ukuran Machine Loker</h2><span class="k-muted">Tentukan kapasitas unit yang paling sesuai.</span></div>', unsafe_allow_html=True)
    sizes = [("Mini Size", "Cocok untuk smartphone & dompet", 8), ("Mid Size", "Ideal untuk tas ransel & laptop", 12), ("Large Size", "Muat koper kabin & jaket tebal", 16), ("Extra Large", "Untuk perlengkapan besar", 24)]
    cols = st.columns(2)
    for idx, (name, desc, slots) in enumerate(sizes):
        with cols[idx % 2]:
            st.markdown(f'<div class="k-card"><h3>{name}</h3><p class="k-muted">{desc}</p><span class="k-chip">{slots} slot awal</span></div>', unsafe_allow_html=True)
            if st.button(f"Pilih {name}", key=f"size_{idx}"):
                form["unit_size"] = name
                form["jumlah_slot"] = slots
    st.info("Pemilihan ukuran machine akan menentukan biaya instalasi dan kapasitas awal.")
    c1, c2, c3 = st.columns([1, 1, 1])
    if c1.button("Kembali"):
        st.session_state["mitra_register_step"] = 1
        st.rerun()
    if c3.button("Lanjut Tahapan", key="step2_next"):
        st.session_state["mitra_register_step"] = 3
        st.rerun()


def render_register_step_confirm():
    form = st.session_state.setdefault("mitra_usaha_form", {})
    left, center, right = st.columns([1, 1.3, 1])
    with center:
        st.markdown('<div class="k-card"><h3>Ringkasan & Validasi</h3>', unsafe_allow_html=True)
        st.write(f"Nama Usaha: **{form.get('nama_usaha', '-')}**")
        st.write(f"Alamat Penempatan: **{form.get('alamat', '-')}**")
        st.write(f"Unit Loker: **{form.get('unit_size', 'Mid Size')}**")
        st.write(f"Jumlah Slot: **{form.get('jumlah_slot', 12)}**")
        agree = st.checkbox("Saya menyetujui syarat dan ketentuan kemitraan KeepIn.")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Kirim Pendaftaran", disabled=not agree):
            payload = {
                "id_owner": int(st.session_state["id_user"]),
                "nama_usaha": form.get("nama_usaha", "Usaha Baru"),
                "alamat": form.get("alamat", "Yogyakarta"),
                "phone": "-",
                "jumlah_slot": int(form.get("jumlah_slot", 12)),
            }
            res = create_usaha(payload)
            if res.status_code == 201:
                st.success("Pendaftaran berhasil dikirim.")
                st.session_state["mitra_register_step"] = 1
                st.session_state["mitra_usaha_form"] = {}
            else:
                st.error(res.text)


def render_usaha_table():
    try:
        res = get_usaha_by_owner(st.session_state["id_user"])
        rows = res.json().get("data", []) if res.status_code == 200 else []
    except Exception:
        rows = []
    if not rows:
        st.info("Belum ada usaha terdaftar.")
        return
    for usaha in rows:
        st.markdown(f'<div class="k-card-soft" style="margin-bottom:10px;"><b>{usaha["nama_usaha"]}</b><br><span class="k-muted">{usaha.get("alamat","-")}</span><br><br><span class="k-chip k-chip-green">{usaha.get("status_verifikasi","MENUNGGU")}</span> <span class="k-chip">{usaha.get("jumlah_slot",0)} slot</span></div>', unsafe_allow_html=True)


def render_laporan_bisnis():
    st.markdown('<div class="welcome-title" style="font-size:28px;">Laporan Performa Bisnis</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    render_metric_card(c1, "Total Pendapatan", "Rp 12.450.000")
    render_metric_card(c2, "Booking Selesai", 128)
    render_metric_card(c3, "Tingkat Hunian", "78%")
    render_metric_card(c4, "Loker Aktif", "24 / 30")
    left, right = st.columns([2, 1])
    with left:
        st.markdown('<div class="k-card"><b>Grafik Pendapatan</b>', unsafe_allow_html=True)
        st.line_chart({"Pendapatan": [5200000, 6100000, 8300000, 7600000, 9100000, 9800000, 12450000]})
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="k-card"><b>Booking Terbaru</b><br><br><span class="k-muted">Malioboro Mall - Loker M</span><br><b>Rp 20.000</b><hr><span class="k-muted">Ambarrukmo Plaza - Loker S</span><br><b>Rp 15.000</b></div>', unsafe_allow_html=True)


def render_aktivitas_loker():
    st.markdown('<div class="welcome-title" style="font-size:22px;">Monitoring Aktivitas Loker</div>', unsafe_allow_html=True)
    search, filt = st.columns([2, 1])
    search.text_input("Cari loker / penyewa", placeholder="Ketik nomor loker atau nama penyewa...")
    filt.selectbox("Filter lokasi usaha", ["Semua Lokasi", "Malioboro Mall", "Ambarrukmo Plaza"])
    activities = [
        ("A-01", "Sedang Digunakan", "Budi Santoso", "2 Jam", "15 Menit", True),
        ("A-02", "Sedang Digunakan", "Siti Aminah", "1 Jam", "Rp 10.000", False),
        ("B-05", "Tersedia", "-", "-", "Menunggu penyewa baru", False),
        ("C-12", "Sedang Digunakan", "Andi Wijaya", "4 Jam", "45 Menit", True),
    ]
    for unit, status, penyewa, durasi, alert, danger in activities:
        border = "#FFB4B4" if danger else "#E6ECF4"
        st.markdown(f'<div class="k-card-soft" style="margin-bottom:14px;border-color:{border};display:flex;justify-content:space-between;align-items:center;"><div><b>{status}</b><br><span class="k-muted">Unit {unit}</span></div><div><span class="k-muted">Penyewa</span><br><b>{penyewa}</b></div><div><span class="k-muted">Durasi</span><br><b>{durasi}</b></div><div><span class="k-chip {"k-chip-green" if not danger else ""}">{alert}</span></div></div>', unsafe_allow_html=True)


def render_penarikan_saldo():
    st.markdown('<div class="welcome-title" style="font-size:22px;">Penarikan Saldo</div>', unsafe_allow_html=True)
    st.markdown('<div class="k-hero-dark" style="max-width:620px;margin:auto;"><span class="k-muted">Total Pendapatan Anda</span><h2>Rp 12.450.000</h2><span class="k-chip">Batas harian Rp 50.000.000</span></div>', unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.3, 1])
    with center:
        st.markdown('<div class="k-card"><h3>Nominal & Metode</h3>', unsafe_allow_html=True)
        nominal = st.number_input("Jumlah penarikan", min_value=50000, value=500000, step=50000)
        method = st.radio("Pilih tujuan pengiriman", ["Bank BCA", "Bank Mandiri", "Bank BNI", "GoPay", "OVO", "DANA"], horizontal=True)
        if st.button("Lanjut Konfirmasi"):
            st.success(f"Pengajuan penarikan Rp {nominal:,.0f} ke {method} berhasil dibuat.")
        st.markdown('</div>', unsafe_allow_html=True)
