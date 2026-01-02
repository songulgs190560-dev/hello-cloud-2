import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            count INTEGER NOT NULL
        );
    """)
    cur.execute("SELECT count FROM visitors WHERE id = 1;")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO visitors (id, count) VALUES (1, 0);")
    conn.commit()
    cur.close()
    conn.close()

@app.before_first_request
def setup():
    init_db()

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE visitors SET count = count + 1 WHERE id = 1;")
    cur.execute("SELECT count FROM visitors WHERE id = 1;")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f"""
    <h1>👋 Hoş geldiniz</h1>
    <h2>👀 Ziyaretçi Sayısı: {count}</h2>
    """

if __name__ == "__main__":
    app.run(debug=True)
