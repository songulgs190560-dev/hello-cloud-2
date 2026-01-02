import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def index():
    if not DATABASE_URL:
        return "DATABASE_URL tanımlı değil ❌"

    conn = connect_db()
    cur = conn.cursor()

    # tablo yoksa oluştur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            count INTEGER
        )
    """)

    # satır yoksa ekle
    cur.execute("SELECT count FROM visitors LIMIT 1")
    row = cur.fetchone()

    if row is None:
        cur.execute("INSERT INTO visitors (count) VALUES (1)")
        visitors = 1
    else:
        visitors = row[0] + 1
        cur.execute("UPDATE visitors SET count = %s", (visitors,))

    conn.commit()
    cur.close()
    conn.close()

    return f"👥 Ziyaretçi Sayısı: {visitors}"

if __name__ == "__main__":
    app.run()
