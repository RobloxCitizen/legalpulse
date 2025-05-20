import sqlite3
import os

db_path = os.path.join(os.getcwd(), "legal_data", "legal_data.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT source, title, link, date FROM news")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()