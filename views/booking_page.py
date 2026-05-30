import streamlit as st
import pandas as pd
import pydeck as pdk

from services.booking_client import create_booking
from services.loker_client import get_lockers


def render_booking_page():
    if "booking_step" not in st.session_state:
        st.session_state["booking_step"] = 1

    render_booking_css()

    if st.session_state["booking_step"] == 1:
        render_booking_locker_selection()
    elif st.session_state["booking_step"] == 2:
        render_booking_confirmation()


def render_booking_css():
    st.markdown("""
        <style>
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
        .filter-title {
            display: inline-block; background: #52D1A2; color: white; border-radius: 8px;
            padding: 13px 22px; margin: 8px 0 12px; font-size: 12px; font-weight: 900;
            text-transform: uppercase; box-shadow: 0 12px 26px rgba(82, 209, 162, 0.35);
        }
        .loker-list-head {
            display: flex; justify-content: space-between; align-items: center;
            color: #94A3B8; font-size: 10px; font-weight: 900; letter-spacing: 1.1px;
            text-transform: uppercase; margin: 18px 0 12px;
        }
        .loker-card {
            background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
            overflow: hidden; box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
            margin-bottom: 14px; text-align: left; padding: 0;
        }
        .loker-visual {
            height: 108px; position: relative;
            background:
                linear-gradient(135deg, rgba(30,41,59,0.10), rgba(82,209,162,0.22)),
                repeating-linear-gradient(90deg, #CBD5E1 0 10px, #E2E8F0 10px 18px);
        }
        .loker-pill, .loker-status {
            position: absolute; top: 10px; border-radius: 999px; padding: 5px 10px;
            font-size: 10px; font-weight: 900; text-transform: uppercase;
        }
        .loker-pill { left: 12px; background: #FFFFFF; color: #0F766E; }
        .loker-status { right: 12px; background: #52D1A2; color: white; }
        .loker-body { padding: 15px; }
        .loker-title { font-size: 16px; font-weight: 900; color: #1E293B; margin-bottom: 4px; }
        .loker-address {
            font-size: 10px; color: #94A3B8; text-transform: uppercase;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .loker-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
        .loker-size { font-size: 11px; color: #64748B; font-weight: 900; text-transform: uppercase; }
        .loker-price { font-size: 20px; font-weight: 900; color: #52D1A2; }
        .loker-unit { font-size: 10px; color: #94A3B8; font-weight: 800; }
        .map-panel {
            min-height: 650px; border-radius: 8px; border: 1px solid #E2E8F0;
            background-color: #F8FAFC; background-image: radial-gradient(#CBD5E1 1px, transparent 1px);
            background-size: 28px 28px; position: relative; overflow: hidden; margin-top: 18px;
        }
        .map-search {
            position: absolute; top: 18px; left: 50%; transform: translateX(-50%);
            background: #FFFFFF; border: 1px solid #E2E8F0; color: #334155;
            border-radius: 999px; padding: 10px 22px; font-size: 12px; font-weight: 800;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.10);
        }
        .map-empty {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: #FFFFFF; border: 1px solid #E2E8F0; color: #64748B;
            border-radius: 8px; padding: 14px 18px; font-size: 13px; font-weight: 800;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }
        .map-marker {
            position: absolute; width: 22px; height: 22px; border-radius: 999px;
            background: #B8A7FF; border: 4px solid #FFFFFF;
            box-shadow: 0 8px 18px rgba(79, 70, 229, 0.25);
        }
        .map-marker.ready { background: #52D1A2; }
        .map-legend {
            position: absolute; left: 24px; right: 24px; bottom: 22px;
            display: flex; justify-content: space-around; background: white;
            border-radius: 999px; padding: 13px 20px; box-shadow: 0 12px 24px rgba(15, 23, 42, 0.10);
            color: #64748B; font-size: 12px; font-weight: 800;
        }
        .dot { display: inline-block; width: 8px; height: 8px; border-radius: 999px; margin-right: 8px; }
        .dot.ready { background: #52D1A2; }
        .dot.warn { background: #F59E0B; }
        .dot.full { background: #F87171; }
        </style>
    """, unsafe_allow_html=True)


def render_booking_locker_selection():
    st.markdown('<div class="welcome-title">Cari Loker Terdekat</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Temukan lokasi penyimpanan aman di area strategis.</div>', unsafe_allow_html=True)

    col_search, col_button = st.columns([5, 1])
    with col_search:
        search_query = st.text_input(
            "Cari loker",
            value="Kuningan, Jakarta Selatan",
            label_visibility="collapsed",
            placeholder="Cari area, mall, atau tipe loker",
        )
    with col_button:
        st.button("Cari Lokasi", use_container_width=True)

    st.markdown('<div class="filter-title">Filter Loker</div>', unsafe_allow_html=True)
    filter_cols = st.columns([1, 1, 1, 4])
    with filter_cols[0]:
        sort_jarak = st.selectbox("Jarak", ["Jarak Terdekat", "Jarak Default"], label_visibility="collapsed")
    with filter_cols[1]:
        sort_harga = st.selectbox("Harga", ["Harga Default", "Harga Termurah", "Harga Tertinggi"], label_visibility="collapsed")
    with filter_cols[2]:
        ukuran_filter = st.selectbox("Ukuran", ["Semua", "Small", "Medium", "Large"], label_visibility="collapsed")

    sort_by = "jarak" if sort_jarak == "Jarak Terdekat" else "harga_asc"
    if sort_harga == "Harga Termurah":
        sort_by = "harga_asc"
    elif sort_harga == "Harga Tertinggi":
        sort_by = "harga_desc"

    try:
        response = get_lockers(search=search_query, sort_by=sort_by, ukuran=ukuran_filter)

        if response.status_code == 200:
            daftar_loker = response.json().get("data", [])

            list_col, map_col = st.columns([1, 3])

            with list_col:
                st.markdown(f'<div class="loker-list-head"><span>{len(daftar_loker)} lokasi di sekitarmu</span><span>Real-time data</span></div>', unsafe_allow_html=True)
                if not daftar_loker:
                    st.info("Belum ada loker READY yang cocok dengan pencarian dan filter Anda.")
                else:
                    for loker in daftar_loker:
                        render_loker_card(loker)
                        if st.button(f"Pilih & Sewa {loker['id_loker']}", use_container_width=True, key=f"btn_{loker['id_loker']}"):
                            st.session_state["temp_id_loker"] = loker['id_loker']
                            st.session_state["temp_tipe"] = loker['tipe_loker']
                            st.session_state["temp_harga"] = loker['harga_per_jam']
                            st.session_state["temp_lokasi"] = loker['lokasi']
                            st.session_state["booking_step"] = 2
                            st.rerun()

            with map_col:
                render_loker_map(daftar_loker)
        else:
            st.error("Gagal memuat data dari Loker Service.")
    except Exception:
        st.error("Gagal terhubung ke `loker_service.py`. Pastikan service Port 8002 aktif!")


def render_loker_card(loker):
    st.markdown(f"""
        <div class="loker-card">
            <div class="loker-visual">
                <div class="loker-pill">{loker.get('jarak_km', 0)} km - {loker.get('estimasi_menit', 0)} menit</div>
                <div class="loker-status">{loker.get('status_label', 'Tersedia')}</div>
            </div>
            <div class="loker-body">
                <div class="loker-title">{loker.get('nama_tempat', 'Loker Terdekat')}</div>
                <div class="loker-address">{loker.get('alamat_ringkas', loker['lokasi'])}</div>
                <div class="loker-meta">
                    <div>
                        <div class="loker-size">Ukuran {loker['tipe_loker']}</div>
                        <div class="loker-unit">Unit {loker['id_loker']}</div>
                    </div>
                    <div>
                        <div class="loker-price">Rp {loker['harga_per_jam']:,.0f}</div>
                        <div class="loker-unit">/jam</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_loker_map(daftar_loker):
    map_rows = [
        {
            "id_loker": loker["id_loker"],
            "nama_tempat": loker.get("nama_tempat", "Loker Terdekat"),
            "lokasi": loker["lokasi"],
            "tipe_loker": loker["tipe_loker"],
            "harga_per_jam": float(loker["harga_per_jam"]),
            "jarak_km": float(loker.get("jarak_km", 0)),
            "latitude": float(loker.get("latitude", -6.2232)),
            "longitude": float(loker.get("longitude", 106.8277)),
        }
        for loker in daftar_loker
    ]

    df = pd.DataFrame(map_rows)
    center_lat = df["latitude"].mean() if not df.empty else -6.2232
    center_lon = df["longitude"].mean() if not df.empty else 106.8277

    layers = []
    if not df.empty:
        layers = [
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[longitude, latitude]",
                get_radius=95,
                get_fill_color=[82, 209, 162, 220],
                get_line_color=[255, 255, 255],
                line_width_min_pixels=2,
                pickable=True,
            ),
            pdk.Layer(
                "TextLayer",
                data=df,
                get_position="[longitude, latitude]",
                get_text="id_loker",
                get_size=12,
                get_color=[30, 41, 59],
                get_angle=0,
                get_text_anchor="'middle'",
                get_alignment_baseline="'bottom'",
            ),
        ]

    deck = pdk.Deck(
        map_style="road",
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=13,
            pitch=0,
        ),
        layers=layers,
        tooltip={
            "html": """
                <b>{nama_tempat}</b><br/>
                Unit {id_loker} - {tipe_loker}<br/>
                Rp {harga_per_jam}/jam<br/>
                {jarak_km} km dari area pencarian<br/>
                <small>{lokasi}</small>
            """,
            "style": {
                "backgroundColor": "#1E293B",
                "color": "white",
                "fontFamily": "Inter, sans-serif",
            },
        },
    )

    if df.empty:
        st.info("Map tetap tampil, tetapi belum ada titik loker READY di area ini.")

    st.pydeck_chart(deck, use_container_width=True)


def render_booking_confirmation():
    if st.button("Kembali Pilih Loker", key="back_to_step1"):
        st.session_state["booking_step"] = 1
        st.rerun()
    
    st.markdown(f'<div class="welcome-title" style="margin-top:10px;">Konfirmasi Penyewaan Loker {st.session_state["temp_id_loker"]}</div>', unsafe_allow_html=True)
    st.write("")

    col_det_left, col_det_right = st.columns([1.3, 1])

    with col_det_left:
        st.markdown("#### Lokasi Penempatan Fisik Loker")
        st.markdown("""
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.307222459998!2d106.8277259747506!3d-6.223165260950669!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f3f4b5003b57%3A0x6bda19a9cf582!2sKuningan%20City!5e0!3m2!1sid!2sid!4v1710000000000!5m2!1sid!2sid" 
            width="100%" height="220" style="border:0; border-radius:12px; margin-bottom:20px;" allowfullscreen="" loading="lazy"></iframe>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Atur Durasi Penggunaan")
        durasi = st.number_input("Berapa hari Anda ingin menyewa loker ini?", min_value=1, max_value=30, value=1, step=1)
        
        st.markdown("#### Metode Pembayaran")
        metode_bayar = st.radio("Pilih Opsi Pembayaran:", ["QRIS (Otomatis)", "Transfer Bank Manual", "KeepIn Wallet"], horizontal=True)

    with col_det_right:
        st.markdown("#### Ringkasan Biaya")
        
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
        
        if st.button("Konfirmasi & Bayar Sekarang", type="primary", use_container_width=True):
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
                    st.success(f"{data_res['message']} (ID Transaksi: #{data_res['booking_id']})")
                    st.balloons()
                    st.session_state["booking_step"] = 1
                    st.session_state["active_menu"] = "Riwayat Booking"
                    st.rerun()
                else:
                    st.error(f"Gagal memproses data booking: {res.json().get('detail')}")
            except Exception:
                st.error("Gagal terhubung ke server backend `booking_service.py` di Port 8001. Pastikan service sudah dinyalakan!")
