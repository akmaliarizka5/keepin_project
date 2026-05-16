import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Inisialisasi Session State untuk Navigasi
if 'page' not in st.session_state:
    st.session_state.page = 'Beranda'

def set_page(page_name):
    st.session_state.page = page_name

# 2. Konfigurasi Halaman & CSS
st.set_page_config(page_title="KeepIn Mitra Dashboard", layout="wide")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #4FD1C5;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-card {
        background-color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #F1F5F9;
        margin-bottom: 20px;
    }
    .status-box {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: 600;
    }
    .dashboard-title { font-size: 28px; font-weight: 700; color: #1E293B; margin-bottom: 0; }
    .dashboard-subtitle { color: #64748B; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI PENGAMBILAN DATA DARI MICROSERVICES VIA HTTP API ---
BASE_URLS = {
    "auth": "http://127.0.0.1:5001",
    "booking": "http://127.0.0.1:5002",
    "inventory": "http://127.0.0.1:5003",
    "payment": "http://127.0.0.1:5004"
}

def fetch_data_from_service(service_name, endpoint):
    try:
        response = requests.get(f"{BASE_URLS[service_name]}{endpoint}", timeout=2)
        if response.status_code == 200:
            return response.json(), "Online"
        return None, f"Error {response.status_code}"
    except Exception:
        return None, "Offline"

# Ambil data dari semua service
bookings_data, booking_status = fetch_data_from_service("booking", "/booking")
payments_data, payment_status = fetch_data_from_service("payment", "/payment")

# Mengonversi data JSON ke Pandas DataFrame jika sukses
df_booking = pd.DataFrame(bookings_data) if bookings_data else pd.DataFrame()
df_payment = pd.DataFrame(payments_data) if payments_data else pd.DataFrame()

# Simulasikan pengambilan data user (id_user=1) untuk menyapa mitra secara dinamis
user_data, auth_status = fetch_data_from_service("auth", "/user/1")
nama_mitra = user_data.get("nama", "Mitra") if user_data and "nama" in user_data else "Mitra"

# --- 4. SIDEBAR DENGAN PANEL STATUS MICROSERVICES ---
with st.sidebar:
    st.markdown("### KeepIn MITRA")
    st.markdown("---")
    st.button("🏠 Beranda", use_container_width=True, on_click=set_page, args=('Beranda',))
    st.button("📋 Pendaftaran Usaha", use_container_width=True, on_click=set_page, args=('Pendaftaran',))
    st.button("📊 Laporan Bisnis", use_container_width=True, on_click=set_page, args=('Laporan',))
    st.markdown("---")
    
    st.markdown("### System Status")
    # Tampilkan status masing-masing service di sidebar secara visual
    for s_name, s_status in [("Auth Service", auth_status), ("Booking Service", booking_status), ("Payment Service", payment_status)]:
        color = "#DEF7EC" if s_status == "Online" else "#FEF3C7" if "Error" in s_status else "#FDE8E8"
        text_color = "#03543F" if s_status == "Online" else "#92400E" if "Error" in s_status else "#9B1C1C"
        st.markdown(f'<div class="status-box" style="background-color: {color}; color: {text_color};">● {s_name}: {s_status}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("⬅️ Keluar", use_container_width=True):
        st.info("Anda telah keluar.")
        st.stop()

# --- 5. LOGIKA PENAMPILAN HALAMAN ---
if st.session_state.page == 'Beranda':
    head_col, filter_col = st.columns([3, 1])
    with head_col:
        st.markdown(f'<p class="dashboard-title">Selamat datang kembali, {nama_mitra}! 👋</p>', unsafe_allow_html=True)
        st.markdown('<p class="dashboard-subtitle">Kelola usaha dan pantau performa cabang bisnis loker Anda.</p>', unsafe_allow_html=True)
    with filter_col:
        st.selectbox("FILTER CABANG", ["Semua Cabang", "Stasiun Gambir", "Mall Kelapa Gading"], label_visibility="collapsed")

    # Banner pendaftaran cabang baru
    st.markdown("""
        <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center; padding: 30px; border: none; background: white;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="background-color: #E6FFFA; padding: 15px; border-radius: 50%; color: #4FD1C5; font-size: 24px; font-weight: bold;">+</div>
                <div>
                    <p style="font-size: 20px; font-weight: 700; margin: 0; color: #1E293B;">Daftarkan Cabang Usaha Baru</p>
                    <p style="font-size: 14px; color: #64748B; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Satu Akun Mitra Bisa Punya Banyak Lokasi Toko Loker.</p>
                </div>
            </div>
            <button style="background-color: #2D3748; color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 700; cursor: pointer;">
                DAFTARKAN CABANG
            </button>
        </div>
    """, unsafe_allow_html=True)

    st.write("") 

    # --- ROW 2: MINI METRICS ---
    c1, c2, c3, c4 = st.columns(4)
    total_booking_count = len(df_booking) if not df_booking.empty else 0
    
    with c1:
        st.markdown("""<div class="metric-card">
            <p style='color:#64748B; font-size:12px; font-weight:600;'>TOTAL USAHA/CABANG</p>
            <p style='font-size:28px; font-weight:700; margin:0;'>2</p>
            <p style='color:#10B981; font-size:12px; margin-top:5px;'>↑ Aktif</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card">
            <p style='color:#64748B; font-size:12px; font-weight:600;'>TOTAL LOKER FISIK</p>
            <p style='font-size:28px; font-weight:700; margin:0;'>15</p>
            <p style='color:#94A3B8; font-size:12px; margin-top:5px;'>Di Inventory Service</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card">
            <p style='color:#64748B; font-size:12px; font-weight:600;'>LOKER TERPAKAI</p>
            <p style='font-size:28px; font-weight:700; margin:0;'>8</p>
            <p style='color:#10B981; font-size:12px; margin-top:5px;'>Status: Terisi</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <p style='color:#64748B; font-size:12px; font-weight:600;'>TOTAL TRANSAKSI SEWA</p>
            <p style='font-size:28px; font-weight:700; margin:0;'>{total_booking_count}</p>
            <p style='color:#10B981; font-size:12px; margin-top:5px;'>Dari Booking Service</p>
        </div>""", unsafe_allow_html=True)

    # --- DAFTAR CABANG USAHA SAYA ---
    st.write("")
    st.markdown('<p style="font-size:14px; font-weight:700; color:#64748B; letter-spacing:1px;">STRUKTUR CABANG DAN OPERASIONAL</p>', unsafe_allow_html=True)
    
    usaha_data = pd.DataFrame({
        "NAMA UNIT CABANG": ["KeepIn Stasiun Gambir", "KeepIn Mall Kelapa Gading"],
        "ALAMAT USAHA": ["Selasar Pintu Utara Stasiun Gambir", "Lantai LG Depan Supermarket"],
        "TOTAL UNIT LOKER": [10, 5],
        "STATUS LEGALITAS": ["Verified", "Verified"]
    })
    st.dataframe(usaha_data, use_container_width=True, hide_index=True)

elif st.session_state.page == 'Laporan':
    st.markdown('<p class="dashboard-title">Laporan Keuangan & Performa Finansial 📈</p>', unsafe_allow_html=True)
    st.markdown('<p class="dashboard-subtitle">Data di bawah diolah langsung dari real-time Payment Service Gateway.</p>', unsafe_allow_html=True)

    if not df_payment.empty:
        # Pre-processing finansial
        df_payment['jumlah_bayar'] = pd.to_numeric(df_payment['jumlah_bayar'])
        df_payment['waktu_bayar'] = pd.to_datetime(df_payment['waktu_bayar'])
        
        total_rev = df_payment[df_payment['status_pembayaran'].str.lower() == 'sukses']['jumlah_bayar'].sum()
        total_trx = len(df_payment)

        # Kartu Ringkasan
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="metric-card"><p style='color:#64748B; font-size:14px;'>TOTAL OMSET REVENUE</p>
            <p style='font-size:24px; font-weight:700; color:#4FD1C5;'>Rp {total_rev:,.2f}</p></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-card"><p style='color:#64748B; font-size:14px;'>JUMLAH INVOICE MASUK</p>
            <p style='font-size:24px; font-weight:700;'>{total_trx} Transaksi</p></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-card"><p style='color:#64748B; font-size:14px;'>GATEWAY UTAMA</p>
            <p style='font-size:24px; font-weight:700; color:#9F7AEA;'>Midtrans / QRIS</p></div>""", unsafe_allow_html=True)

        # --- GRAFIK PENDAPATAN & LOG DATA ---
        chart_col, list_col = st.columns([2, 1])
        with chart_col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Tren Omset Keuangan harian")
            daily_rev = df_payment.groupby(df_payment['waktu_bayar'].dt.date)['jumlah_bayar'].sum().reset_index()
            fig_line = px.line(daily_rev, x='waktu_bayar', y='jumlah_bayar', markers=True, color_discrete_sequence=['#4FD1C5'])
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with list_col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Daftar Invoice Terakhir")
            st.dataframe(df_payment[['invoice_number', 'jumlah_bayar', 'status_pembayaran']].tail(5), hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak dapat memuat laporan finansial. Pastikan payment_service sudah aktif dan memiliki data dummy.")

elif st.session_state.page == 'Pendaftaran':
    st.title("📋 Menu Pendaftaran Cabang Baru")
    st.write("Gunakan formulir ini untuk menambah jaringan bisnis loker baru di bawah naungan ID legalitas Anda.")