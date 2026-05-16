import os
from flask import Flask, jsonify, request
# Import helper dan koneksi khusus booking
from database import fetch_one, fetch_all, get_booking_db_conn

app = Flask(__name__)

# Endpoint untuk mengambil semua data pesanan
@app.route('/booking', methods=['GET'])
def get_all_bookings():
    try:
        query = "SELECT * FROM pesanan ORDER BY id_pesanan DESC"
        bookings = fetch_all(get_booking_db_conn, query)
        return jsonify(bookings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mengambil satu data pesanan spesifik berdasarkan ID
@app.route('/booking/<int:id_pesanan>', methods=['GET'])
def get_booking_by_id(id_pesanan):
    try:
        query = "SELECT * FROM pesanan WHERE id_pesanan = %s"
        booking = fetch_one(get_booking_db_conn, query, (id_pesanan,))
        if booking:
            return jsonify(booking), 200
        return jsonify({"error": "Data booking tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Booking service berjalan di port 5002
    app.run(host='0.0.0.0', port=5002, debug=True)