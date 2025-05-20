import streamlit as st
from rag import setup_rag, query_rag
from datetime import datetime, timedelta

st.title("LegalPulse")

if "requests" not in st.session_state:
    st.session_state.requests = []

REQUEST_LIMIT = 80
TIME_WINDOW = timedelta(hours=3)

def check_limit():
    now = datetime.now()
    st.session_state.requests = [t for t in st.session_state.requests if now - t < TIME_WINDOW]
    if len(st.session_state.requests) >= REQUEST_LIMIT:
        st.error(f"Лимит {REQUEST_LIMIT} запросов за 3 часа превышен. Подождите.")
        return False
    return True

try:
    vectorstore, model = setup_rag()
except Exception as e:
    st.error(f"Ошибка инициализации: {e}")
    st.stop()

query = st.text_input("Введите запрос, например: Как оформить ИП в РБ в 2025?")
if st.button("Получить ответ"):
    if not query.strip():
        st.error("Пожалуйста, введите запрос.")
    elif check_limit():
        try:
            answer = query_rag(vectorstore, model, query)
            st.write(answer)
            st.session_state.requests.append(datetime.now())
        except Exception as e:
            st.error(f"Ошибка запроса: {e}")