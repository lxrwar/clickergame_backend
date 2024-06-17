from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='frontend/build')

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

def get_db():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/update_score', methods=['POST'])
def update_score():
    user_id = request.json['user_id']
    score = request.json['score']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (user_id, score) VALUES (%s, %s) ON DUPLICATE KEY UPDATE score=%s", (user_id, score, score))
    db.commit()
    db.close()
    return jsonify({"status": "success"}), 200

@app.route('/get_score', methods=['GET'])
def get_score():
    user_id = request.args.get('user_id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id = %s", (user_id,))
    score = cursor.fetchone()
    db.close()
    return jsonify({"score": score[0] if score else 0}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
