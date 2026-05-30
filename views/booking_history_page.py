import streamlit as st

from services.booking_client import get_user_bookings


def render_booking_history_page():
    st.subheader("📜 Riwayat Penggunaan Loker Anda")
    
    try:
        res = get_user_bookings(st.session_state['id_user'])
        if res.status_code == 200:
            daftar_booking = res.json()["data"]
            
            if not daftar_booking:
                st.info("Belum ada transaksi pemesanan loker.")
            else:
                for b in daftar_booking:
                    with st.expander(f"📦 Order ID #{b['id_booking']} - {b['nama_tempat']} ({b['status_booking']})"):
                        st.write(f"- **Unit Loker:** {b['id_loker']}")
                        st.write(f"- **Tanggal Transaksi:** {b['tgl_booking']}")
                        st.write(f"- **Durasi Sewa:** {b['durasi_sewa']} Hari")
                        st.markdown(f"- **Total Bayar:** <span style='color:#52D1A2; font-weight:bold;'>Rp {b['total_biaya']:,.0f}</span>", unsafe_allow_html=True)
        else:
            st.error("❌ Gagal menarik data riwayat booking.")
    except Exception:
        st.error("❌ Tidak bisa memuat riwayat. Pastikan backend `booking_service.py` (Port 8001) berjalan.")
