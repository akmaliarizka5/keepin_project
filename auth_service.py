import os
from flask import Flask, jsonify, request
from database import fetch_one, get_auth_db_conn

app = Flask(__name__)

# ENDPOINT 1: Mengambil Data Profil User Berdasarkan ID (Sudah ada sebelumnya)
@app.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user):
    try:
        user = fetch_one(get_auth_db_conn, "SELECT id_user, nama, email, no_hp, role FROM users WHERE id_user = %s", (id_user,))
        return jsonify(user) if user else (jsonify({"error": "User Not Found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ENDPOINT 2: Autentikasi Login (BARU)
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role') # 'mitra', 'penyewa', atau 'admin'

        # Query pencocokan kredensial dasar
        query = "SELECT id_user, nama, email, role FROM users WHERE email = %s AND password_hash = %s AND LOWER(role) = %s"
        user = fetch_one(get_auth_db_conn, query, (email, password, role.lower()))
        
        if user:
            return jsonify({"status": "success", "user": user}), 200
        return jsonify({"status": "fail", "message": "Email, password, atau role tidak sesuai"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ENDPOINT 3: Pendaftaran Akun Baru / Sign Up (BARU)
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        nama = data.get('nama')
        email = data.get('email')
        password = data.get('password')
        no_hp = data.get('no_hp', '')
        role = data.get('role', 'mitra')

        conn = get_auth_db_conn()
        cur = conn.cursor()
        
        # Cek apakah email sudah terdaftar
        cur.execute("SELECT id_user FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"status": "fail", "message": "Email sudah terdaftar!"}), 400

        # Insert user baru ke database auth
        query = "INSERT INTO users (nama, email, password_hash, no_hp, role) VALUES (%s, %s, %s, %s, %s) RETURNING id_user"
        cur.execute(query, (nama, email, password, no_hp, role.lower()))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "User berhasil didaftarkan", "id_user": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)