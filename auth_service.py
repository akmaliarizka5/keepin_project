from flask import Flask, jsonify
# Import fungsi helper dan fungsi koneksinya
from database import fetch_one, get_auth_db_conn, RealDictCursor

app = Flask(__name__)

@app.route('/user/<int:id_user>')
def get_user(id_user):
    try:
        # Masukkan fungsi koneksi auth sebagai parameter pertama
        user = fetch_one(get_auth_db_conn, "SELECT * FROM users WHERE id_user = %s", (id_user,))
        return jsonify(user) if user else (jsonify({"error": "User Not Found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)