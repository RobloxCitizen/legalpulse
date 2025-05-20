import sqlite3
import os

def clean_db():
    db_path = os.path.join("legal_data", "legal_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Удаляем записи с "Нет заголовка" или пустым pdf_text
    cursor.execute("DELETE FROM news WHERE title = 'Нет заголовка' OR pdf_text IS NULL OR pdf_text = ''")
    deleted = cursor.rowcount

    # Удаляем дубликаты по link и pdf_text
    cursor.execute("""
        DELETE FROM news WHERE id NOT IN (
            SELECT MIN(id) FROM news GROUP BY link, pdf_text
        )
    """)
    deleted += cursor.rowcount

    conn.commit()
    conn.close()
    print(f"Удалено {deleted} некорректных записей")

if __name__ == "__main__":
    clean_db()