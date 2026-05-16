from flask import Flask, jsonify
from database import get_auth_db_conn, RealDictCursor

app = Flask(__name__)

@app.route('/user/<int:id_user>')
def get_user(id_user):
    try:
        conn = get_auth_db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM penyewa WHERE id_user = %s', (id_user,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(user) if user else (jsonify({"error": "Not Found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)