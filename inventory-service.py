from flask import Flask, jsonify
from database import fetch_one, get_inventory_db_conn, RealDictCursor

app = Flask(__name__)

@app.route('/loker/<int:id_loker>')
def get_loker(id_loker):
    try:
        loker = fetch_one(get_inventory_db_conn, "SELECT * FROM loker WHERE id_loker = %s", (id_loker,))
        return jsonify(loker) if loker else (jsonify({"error": "Loker Not Found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5003)