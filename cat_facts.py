import requests
import sqlite3

# 1. API İsteği Gönderme
response = requests.get("https://cat-fact.herokuapp.com/facts")
data = response.json()

# 2. Veritabanı Oluşturma
conn = sqlite3.connect('cat_facts.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS facts
                  (id TEXT PRIMARY KEY, text TEXT, type TEXT, user TEXT, upvotes INTEGER)''')

# 3. Veri Kaydetme
for fact in data:
    cursor.execute('''INSERT OR REPLACE INTO facts (id, text, type, user, upvotes)
                      VALUES (?, ?, ?, ?, ?)''',
                   (fact['_id'], fact['text'], fact['type'], fact.get('user', ''), fact.get('upvotes', 0)))

conn.commit()

# 4. Veri Görüntüleme
cursor.execute("SELECT * FROM facts")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Veritabanı bağlantısını kapatma
conn.close()
