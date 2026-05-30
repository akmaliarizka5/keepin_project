import streamlit as st

from services.booking_client import get_user_bookings
from services.payment_client import get_payment_by_booking, update_payment_status


def render_booking_history_page():
    st.subheader("Riwayat Penggunaan Loker")

    try:
        res = get_user_bookings(st.session_state["id_user"])
        if res.status_code != 200:
            st.error("Gagal menarik data riwayat booking.")
            return

        daftar_booking = res.json()["data"]
        if not daftar_booking:
            st.info("Belum ada transaksi pemesanan loker.")
            return

        for booking in daftar_booking:
            status = booking.get("status_booking", "PENDING")
            title = f"Order #{booking['id_booking']} - {booking['nama_tempat']} ({status})"
            with st.expander(title):
                col_info, col_pay = st.columns([2, 1])
                with col_info:
                    st.write(f"Unit Loker: **{booking['id_loker']}**")
                    st.write(f"Tanggal Transaksi: **{booking.get('created_at', '-')}**")
                    st.write(f"Durasi Sewa: **{booking['durasi_sewa']} Jam**")
                    st.write(f"Metode Bayar: **{booking.get('metode_bayar', 'QRIS')}**")
                    st.markdown(f"Total Bayar: <span style='color:#52D1A2; font-weight:bold;'>Rp {booking['total_biaya']:,.0f}</span>", unsafe_allow_html=True)

                with col_pay:
                    render_payment_panel(booking["id_booking"])
    except Exception:
        st.error("Tidak bisa memuat riwayat. Pastikan booking_service.py dan payment_service.py berjalan.")


def render_payment_panel(booking_id):
    try:
        res = get_payment_by_booking(booking_id)
        payment = res.json().get("data") if res.status_code == 200 else None
    except Exception:
        payment = None

    if not payment:
        st.info("Payment belum dibuat.")
        return

    st.caption("Payment")
    st.write(f"Ref: **{payment['reference']}**")
    st.write(f"Status: **{payment['status']}**")

    if payment["status"] == "PENDING":
        if st.button("Tandai Sudah Bayar", key=f"pay_{payment['id_payment']}"):
            update_payment_status(payment["id_payment"], "PAID")
            st.success("Payment ditandai PAID.")
            st.rerun()
