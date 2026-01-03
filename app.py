from flask import Flask, request, render_template_string
import os
import psycopg2

app = Flask(__name__)

def connect_db():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    return psycopg2.connect(DATABASE_URL, sslmode="require")

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Ziyaretçi Defteri</title>
</head>
<body>
    <h2>Ziyaretçi Defteri</h2>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adınız" required>
        <textarea name="mesaj" placeholder="Mesajınız" required></textarea>
        <button type="submit">Gönder</button>
    </form>
    <hr>
    {% for isim, mesaj in mesajlar %}
        <p><strong>{{ isim }}:</strong> {{ mesaj }}</p>
    {% endfor %}
</body>
</html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mesajlar (
            id SERIAL PRIMARY KEY,
            isim TEXT,
            mesaj TEXT
        )
    """)
    conn.commit()

    if request.method == "POST":
        isim = request.form.get("isim")
        mesaj = request.form.get("mesaj")
        if isim and mesaj:
            cur.execute(
                "INSERT INTO mesajlar (isim, mesaj) VALUES (%s, %s)",
                (isim, mesaj)
            )
            conn.commit()

    cur.execute("SELECT isim, mesaj FROM mesajlar ORDER BY id DESC")
    mesajlar = cur.fetchall()

    cur.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, mesajlar=mesajlar)
