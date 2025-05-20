import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
try:
    import serpapi
except ImportError:
    serpapi = None

load_dotenv()

def search_pravo(query):
    if not serpapi or os.getenv("SERPAPI_API_KEY") == "your-serpapi-key":
        return [{
            "source": "pravo.by",
            "title": "Законопроект об амнистии 2025",
            "link": "https://pravo.by/test",
            "date": "2025-04-26",
            "pdf": None,
            "pdf_text": "Депутаты приняли законопроект об амнистии в связи с 80-летием Победы в ВОВ."
        }]
    params = {
        "engine": "google",
        "q": f"{query} site:pravo.by",
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    try:
        search = serpapi.search(params)
        results = search.get("organic_results", [])
        return [{
            "source": "pravo.by",
            "title": r.get("title", "Нет заголовка"),
            "link": r.get("link", "https://pravo.by"),
            "date": r.get("date", "2025-05-20"),
            "pdf": None,
            "pdf_text": r.get("snippet", "")[:1000]
        } for r in results if r.get("title") and r.get("snippet")]
    except Exception as e:
        print(f"Ошибка поиска pravo.by: {e}")
        return []

def save_to_db(data):
    os.makedirs("legal_data", exist_ok=True)
    db_path = os.path.join("legal_data", "legal_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT,
            date TEXT,
            pdf TEXT,
            pdf_text TEXT,
            fetched_at TIMESTAMP
        )
    """)
    for item in data:
        if item["title"] == "Нет заголовка" or not item["pdf_text"]:
            continue
        cursor.execute("SELECT pdf_text FROM news WHERE link = ?", (item["link"],))
        existing = cursor.fetchone()
        if existing and existing[0] == item["pdf_text"]:
            continue
        cursor.execute("""
            INSERT INTO news (source, title, link, date, pdf, pdf_text, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item["source"], item["title"], item["link"], item["date"], item["pdf"], item["pdf_text"], datetime.now()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    query = "законопроект амнистия"
    results = search_pravo(query)
    save_to_db(results)
    print(f"Собрано с pravo.by: {len(results)} записей")