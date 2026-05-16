import streamlit as st
import requests
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="KeepIn Admin Panel", layout="wide")

st.title("📂 LokerKu: Integrated Microservices Dashboard")
st.markdown("---")

# Sidebar untuk status sistem
st.sidebar.header("System Status")
services = {
    "Auth Service": "http://127.0.0.1:5001/user/1",
    "Booking Service": "http://127.0.0.1:5002/all-bookings",
    "Inventory Service": "http://127.0.0.1:5003/loker/1"
}

for name, url in services.items():
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200:
            st.sidebar.success(f"● {name}: Online")
        else:
            st.sidebar.warning(f"○ {name}: Error {res.status_code}")
    except:
        st.sidebar.error(f"○ {name}: Offline")

# Main Content
st.subheader("Daftar Transaksi Gabungan")
st.info("Data di bawah ini ditarik dari Booking Service, yang secara otomatis mengambil detail nama dari Auth Service.")

if st.button("🔄 Refresh Data Transaksi"):
    try:
        # Menembak Booking Service sebagai Aggregator
        response = requests.get("http://127.0.0.1:5002/all-bookings")
        
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                # Menampilkan tabel dengan gaya Streamlit
                st.dataframe(df, use_container_width=True)
            else:
                st.write("Belum ada data transaksi.")
        else:
            st.error("Gagal mengambil data dari Booking Service.")
            
    except Exception as e:
        st.error(f"Koneksi gagal! Pastikan semua file .py sudah dijalankan di terminal. \nDetail: {e}")

st.markdown("---")
st.caption("KeepIn v1.0 - Arsitektur Microservices dengan PostgreSQL")