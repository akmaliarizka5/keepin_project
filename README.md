# 📦 KeepIn Microservices System

Aplikasi manajemen loker berbasis Microservices menggunakan Python (Flask & Streamlit).

## Struktur Arsitektur
- **Auth Service**: Port 5001 (Data User)
- **Booking Service**: Port 5002 (Data Pesanan + API Call ke Auth)
- **Frontend Dashboard**: Streamlit (Visualisasi Data)

## Cara Menjalankan
1. Install dependensi: `pip install flask requests streamlit pandas`
2. Jalankan Auth Service: `python auth_service.py`
3. Jalankan Booking Service: `python booking_service.py`
4. Jalankan Frontend: `streamlit run app.py`