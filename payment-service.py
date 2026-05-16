from flask import Flask, jsonify
from database import fetch_one

app = Flask(__name__)

@app.route('/payment-status/<int:id_pesanan>')
def check_payment(id_pesanan):
    payment = fetch_one("payment_db", "SELECT * FROM pembayaran WHERE id_pesanan = %s", (id_pesanan,))
    return jsonify(payment) if payment else (jsonify({"error": "No Payment Found"}), 404)

if __name__ == '__main__':
    app.run(port=5004)