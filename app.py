import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL YOK")
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route("/")
def index():
    return "Render Flask çalışıyor 🚀"

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT,
            sehir TEXT
        )
    """)

    if request.method == "POST":
        data = request.get_json()
        cur.execute(
            "INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)",
            (data["isim"], data["sehir"])
        )
        conn.commit()

    cur.execute("SELECT isim, sehir FROM ziyaretciler")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)
