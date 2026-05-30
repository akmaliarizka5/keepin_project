import streamlit as st

from services.booking_client import create_booking
from services.loker_client import get_lockers_by_location


def render_booking_page():
    if "booking_step" not in st.session_state:
        st.session_state["booking_step"] = 1

    st.markdown("""
        <style>
        .loker-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            transition: transform 0.2s, border-color 0.2s;
        }
        .loker-card:hover {
            transform: translateY(-2px);
            border-color: #52D1A2;
        }
        .loker-title { font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
        .loker-size { font-size: 13px; color: #64748B; font-weight: 600; text-transform: uppercase; margin-bottom: 15px; }
        .loker-price { font-size: 20px; font-weight: 800; color: #52D1A2; margin-bottom: 5px; }
        .loker-unit { font-size: 12px; color: #94A3B8; }
        
        /* Ringkasan Pembayaran */
        .summary-card {
            background-color: #F8FAFC;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #E2E8F0;
        }
        .summary-row {
            display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; color: #475569;
        }
        .summary-total {
            display: flex; justify-content: space-between; margin-top: 15px; padding-top: 15px;
            border-top: 1px dashed #CBD5E1; font-size: 18px; font-weight: 700; color: #1E293B;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state["booking_step"] == 1:
        render_booking_locker_selection()
    elif st.session_state["booking_step"] == 2:
        render_booking_confirmation()


def render_booking_locker_selection():
    st.markdown('<div class="welcome-title">Cari & Pesan Loker Strategis 📍</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Temukan tempat penitipan barang terbaik dengan sistem keamanan digital 24 jam.</div>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        lokasi_pilihan = st.selectbox("Pilih Lokasi / Mall terdekat:", ["Kuningan City Mall, Jakarta Selatan", "Mall Ambasador, Jakarta Selatan", "Kota Kasablanka, Jakarta Selatan"])
    with col_f2:
        st.write("##")
        st.button("🔍 Perbarui Lokasi", use_container_width=True)
    
    st.markdown("---")
    st.markdown(f"### 📦 Unit Loker Tersedia di **{lokasi_pilihan.split(',')[0]}**")
    st.write("")

    try:
        response = get_lockers_by_location(lokasi_pilihan)
        
        if response.status_code == 200:
            daftar_loker = response.json().get("data", [])
            
            if not daftar_loker:
                st.warning(f"⚠️ Maaf, saat ini tidak ada unit loker yang siap ('READY') di {lokasi_pilihan}.")
            else:
                cols = st.columns(3)
                for idx, loker in enumerate(daftar_loker):
                    col_aktif = cols[idx % 3]
                    
                    with col_aktif:
                        st.markdown(f"""
                            <div class="loker-card">
                                <div class="loker-title">📦 Unit {loker['id_loker']}</div>
                                <div class="loker-size">Tipe: {loker['tipe_loker']}</div>
                                <div class="loker-price">Rp {loker['harga_per_jam']:,.0f}</div>
                                <div class="loker-unit">per jam</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.write("")
                        
                        if st.button(f"Pilih & Sewa {loker['id_loker']}", use_container_width=True, key=f"btn_{loker['id_loker']}"):
                            st.session_state["temp_id_loker"] = loker['id_loker']
                            st.session_state["temp_tipe"] = loker['tipe_loker']
                            st.session_state["temp_harga"] = loker['harga_per_jam']
                            st.session_state["temp_lokasi"] = loker['lokasi']
                            st.session_state["booking_step"] = 2
                            st.rerun()
        else:
            st.error("❌ Gagal memuat data dari Loker Service.")
    except Exception:
        st.error("❌ Gagal terhubung ke `loker_service.py`. Pastikan service Port 8002 aktif!")


def render_booking_confirmation():
    if st.button("⬅ Kembali Pilih Loker", key="back_to_step1"):
        st.session_state["booking_step"] = 1
        st.rerun()
    
    st.markdown(f'<div class="welcome-title" style="margin-top:10px;">Konfirmasi Penyewaan Loker {st.session_state["temp_id_loker"]} 📝</div>', unsafe_allow_html=True)
    st.write("")

    col_det_left, col_det_right = st.columns([1.3, 1])

    with col_det_left:
        st.markdown("#### 📍 Lokasi Penempatan Fisik Loker")
        st.markdown("""
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.307222459998!2d106.8277259747506!3d-6.223165260950669!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f3f4b5003b57%3A0x6bda19a9cf582!2sKuningan%20City!5e0!3m2!1sid!2sid!4v1710000000000!5m2!1sid!2sid" 
            width="100%" height="220" style="border:0; border-radius:12px; margin-bottom:20px;" allowfullscreen="" loading="lazy"></iframe>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📆 Atur Durasi Penggunaan")
        durasi = st.number_input("Berapa hari Anda ingin menyewa loker ini?", min_value=1, max_value=30, value=1, step=1)
        
        st.markdown("#### 💳 Metode Pembayaran")
        metode_bayar = st.radio("Pilih Opsi Pembayaran:", ["QRIS (Otomatis)", "Transfer Bank Manual", "KeepIn Wallet"], horizontal=True)

    with col_det_right:
        st.markdown("#### 📊 Ringkasan Biaya")
        
        total_harga = durasi * st.session_state["temp_harga"]
        
        st.markdown(f"""
            <div class="summary-card">
                <div class="summary-row"><span>Lokasi</span><strong>{st.session_state['temp_lokasi']}</strong></div>
                <div class="summary-row"><span>ID Loker</span><strong>{st.session_state['temp_id_loker']}</strong></div>
                <div class="summary-row"><span>Tipe / Ukuran</span><strong>{st.session_state['temp_tipe']}</strong></div>
                <div class="summary-row"><span>Harga Satuan</span><strong>Rp {st.session_state['temp_harga']:,.0f} / Hari</strong></div>
                <div class="summary-row"><span>Durasi Kontrak</span><strong>{durasi} Hari</strong></div>
                <div class="summary-row"><span>Metode</span><strong>{metode_bayar}</strong></div>
                <div class="summary-total"><span>Total Tagihan</span><span>Rp {total_harga:,.0f}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        if st.button("Konfirmasi & Bayar Sekarang 🚀", type="primary", use_container_width=True):
            payload_booking = {
                "id_user": int(st.session_state["id_user"]),
                "id_loker": str(st.session_state["temp_id_loker"]),
                "nama_tempat": str(st.session_state["temp_lokasi"]),
                "durasi_sewa": int(durasi),
                "total_biaya": float(total_harga)
            }
            
            try:
                res = create_booking(payload_booking)
                
                if res.status_code == 201:
                    data_res = res.json()
                    st.success(f"🎉 {data_res['message']} (ID Transaksi: #{data_res['booking_id']})")
                    st.balloons()
                    st.session_state["booking_step"] = 1
                    st.session_state["active_menu"] = "Riwayat Booking"
                    st.rerun()
                else:
                    st.error(f"❌ Gagal memproses data booking: {res.json().get('detail')}")
            except Exception:
                st.error("❌ Gagal terhubung ke server backend `booking_service.py` di Port 8001. Pastikan service sudah dinyalakan!")
