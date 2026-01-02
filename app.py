import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL
        );
    """)
    cur.execute("SELECT count FROM visitors WHERE id = 1;")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO visitors (id, count) VALUES (1, 0);")
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    if not DATABASE_URL:
        return "DATABASE_URL tanımlı değil ❌"

    ensure_table()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE visitors SET count = count + 1 WHERE id = 1;")
    cur.execute("SELECT count FROM visitors WHER
