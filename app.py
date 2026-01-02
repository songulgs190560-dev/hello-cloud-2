from flask import Flask, render_template_string, request
import os
import psycopg2

app=Flask (__name__

DATABASE_URL = os.getentv("DATABASE_URL"," ")

HTML = " " "
<!doctype html>
<html>
<head>
   <title>Buluttan Selam!</title>
   <style>
        body  {  fony-family: Arial; text_align: center; padding: 50px; backgraund: #eef2f3; }
        h1    {  color:  #333;  }
        form  {  margin:  20px auto;  }
        input {padding:  10px; font-size:  16px;  }
        button {padding:  10px  15px; backgraund:  #4CAF50; color:white border: none; border-radius: 6px; cursor: pointer; }
        ul  { list-style: none;  padding: 0;  }
        li  { backgraund: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
   </style>
</head>
<body>
  <h1>Buluttan Selam!</h1>
  <p>Songül, Merhaba </p>
  <form method="POST">
            <input type="text" name="isim"  placeholder="Songül" required>
            </form>
            <h3>ziyaretçiler:</h3>
            <ul>
               {% for ad in isimler % }
                 <li>{{ ad }}</li>
               {% endfor %}
           </ul>
</body>
</html>
"""


def connect_db():
  conn = psycopg2.connect(DATABASE_URL)
  return conn
@app.route("/", methods=["GET" , "POST"])
def index():
  conn = connect_db()
  cur = conn.cursor()
  cur.execute=("CREATE TABLE IF NOT EXISTS ziyaretçiler (id SERIAL PRIMARY KEY, isim TEXT)")


  if request.method=="POST":
     isim=request.from.get("isim")
     if isim:
       cur.execute("INSERT INTO ziyaretçiler (isim) VALUES (%s)", (isim,))
       conn.commit()

       cur.execute("SELECT isim FROM ziyaretçiler ORDER BY id DESC LIMIT 10")
       isimler = [row[0] for row in cur.fetchal()]

       cur.close()
       conn.close()
       return  render_template_string(HTML, isimler=isimler)

       if__name__=="__main__":
            app.run(host="0.0.0.0", port=5000)
     
  
                 
