from flask import Flask, jsonify
import requests
from database import fetch_all

app = Flask(__name__)

@app.get('/all-bookings')
def all_bookings():
    # 1. Ambil semua pesanan dari booking_db
    bookings = fetch_all("BOOKING_DB_NAME", "SELECT * FROM pesanan")
    
    results = []
    for b in bookings:
        # 2. Panggil Auth Service untuk Nama
        user_res = requests.get(f"http://127.0.0.1:5001/user/{b['id_penyewa']}").json()
        
        # 3. Panggil Inventory Service untuk Detail Loker
        loker_res = requests.get(f"http://127.0.0.1:5003/loker/{b['id_loker']}").json()
        
        results.append({
            "id_pesanan": b['id_pesanan'],
            "nama_penyewa": user_res.get('nama_penyewa', 'Unknown'),
            "nomor_loker": loker_res.get('nomor_loker', 'Unknown'),
            "total_biaya": float(b['total_biaya']),
            "status": b['status_pemesanan']
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5002)