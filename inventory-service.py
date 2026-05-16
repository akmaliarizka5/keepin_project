from flask import Flask, jsonify
from database import fetch_one

app = Flask(__name__)

@app.route('/loker/<int:id_loker>')
def get_loker(id_loker):
    loker = fetch_one("inventory_db", "SELECT * FROM loker WHERE id_loker = %s", (id_loker,))
    return jsonify(loker) if loker else (jsonify({"error": "Loker Not Found"}), 404)

if __name__ == '__main__':
    app.run(port=5003)