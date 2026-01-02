import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    if not DATABASE_URL:
        return None
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def index():
    if not DATABASE_URL:
        return "Uygulama çalışıyor 🚀 (DATABASE_URL tanımlı değil)"

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    cur.close()
    conn.close()
    return "Veritabanı bağlantısı başarılı 🎉"

if __name__ == "__main__":
    app.run(debug=True)
