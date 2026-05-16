import os
from flask import Flask, jsonify, request
# Import helper dan koneksi khusus payment
from database import fetch_one, fetch_all, get_payment_db_conn

app = Flask(__name__)

# Endpoint untuk mengambil semua riwayat pembayaran/invoice
@app.route('/payment', methods=['GET'])
def get_all_payments():
    try:
        query = "SELECT * FROM transaksi_pembayaran ORDER BY id_pembayaran DESC"
        payments = fetch_all(get_payment_db_conn, query)
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk melihat status pembayaran per pesanan
@app.route('/payment/booking/<int:id_pesanan>', methods=['GET'])
def get_payment_by_booking(id_pesanan):
    try:
        query = "SELECT * FROM transaksi_pembayaran WHERE id_pesanan = %s"
        payment = fetch_one(get_payment_db_conn, query, (id_pesanan,))
        if payment:
            return jsonify(payment), 200
        return jsonify({"error": "Riwayat pembayaran belum ada untuk pesanan ini"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Payment service berjalan di port 5004
    app.run(host='0.0.0.0', port=5004, debug=True)