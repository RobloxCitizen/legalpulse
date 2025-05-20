from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import sqlite3
import os
import requests
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

def load_data_from_db():
    db_path = os.path.join("legal_data", "legal_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, link, date, pdf_text FROM news")
    data = cursor.fetchall()
    conn.close()
    return [{"text": row[0] + "\n" + (row[3] or ""), "source": row[1], "date": row[2]} for row in data]

def setup_rag():
    documents = load_data_from_db()
    if not documents:
        raise ValueError("Нет данных в базе")
    doc_objects = [Document(page_content=doc["text"], metadata={"source": doc["source"], "date": doc["date"]}) for doc in documents]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(doc_objects)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings)
    
    xai_api_key = os.getenv("XAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if xai_api_key and xai_api_key != "your-xai-api-key":
        def model(prompt):
            headers = {"Authorization": f"Bearer {xai_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "grok-3",
                "prompt": prompt,
                "max_tokens": 500
            }
            response = requests.post("https://api.x.ai/v1/completions", headers=headers, json=data)
            return response.json().get("choices", [{}])[0].get("text", "Ошибка API")
    elif openai_api_key and openai_api_key != "your-openai-key":
        def model(prompt):
            headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Ошибка API")
    else:
        model = lambda x: "Ответ недоступен: требуется API-ключ xAI или OpenAI."
    
    return vectorstore, model

def query_rag(vectorstore, model, query):
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata["source"] for doc in docs]
    prompt = f"""
    Ответь на запрос: {query}
    Используй ТОЛЬКО эту информацию: {context}
    Источники: {', '.join(sources)}
    Пиши юридическим языком, ссылайся на источники. Не добавляй собственные слова, интерпретации или предположения.
    Если данных недостаточно, напиши: "Информации недостаточно."
    """
    return model(prompt)

if __name__ == "__main__":
    vectorstore, model = setup_rag()
    query = "Как оформить ИП в РБ в 2025?"
    answer = query_rag(vectorstore, model, query)
    print(answer)