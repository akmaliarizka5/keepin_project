import streamlit as st


def render_mitra_page(role_aktif, menu_aktif):
    st.title(f"🏢 Panel Dashboard {role_aktif} — {menu_aktif}")
    
    if menu_aktif == "Beranda":
        st.markdown("### Selamat datang kembali, Owner Mitra Bisnis! 📈")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Loker Dimiliki", "48 Unit", "+12% Bulan Ini")
        col_m2.metric("Loker Aktif Disewa", "36 Unit", "Sangat Produktif")
        col_m3.metric("Total Akumulasi Transaksi", "128 Transaksi", "Grafik Naik")
        
    elif menu_aktif == "Pendaftaran Usaha":
        st.subheader("➕ Daftarkan Titik Lokasi Usaha Loker Baru")
        st.text_input("Nama Tempat / Usaha Loker")
        st.text_area("Alamat Lengkap Unit")
        st.number_input("Jumlah Slot Loker yang Disediakan", min_value=1)
        st.button("Ajukan Verifikasi Lokasi")
        
    elif menu_aktif == "Laporan Bisnis":
        st.subheader("📊 Analisis Keuangan & Omset Pendapatan")
        st.write("Grafik laporan laba-rugi bisnis loker Anda akan dikalkulasikan di sini.")
        
    elif menu_aktif == "Aktivitas Loker":
        st.subheader("🔍 Monitoring Real-Time Penggunaan Unit Loker")
        st.markdown("🟢 **Unit A-01:** Sedang digunakan oleh Budi Santoso (Sisa Waktu: 2 Jam)")
        st.markdown("⚪ **Unit A-02:** Tersedia (Kosong)")
        
    elif menu_aktif == "Penarikan Saldo":
        st.subheader("💳 Tarik Pendapatan Bisnis Loker")
        st.metric("Saldo Siap Cair", "Rp 4.520.000")
        st.button("Tarik Dana ke Rekening Utama")
