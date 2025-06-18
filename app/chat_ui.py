# chat_ui.py
import requests
import streamlit as st

st.title("💬 RAG-powered Chatbot (Cohere)")

api_url = "http://localhost:8000/ask"
chat_history = []

# Text input box
user_input = st.text_input("Ask a question")

if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        response = requests.post(api_url, json={"question": user_input})
        if response.status_code == 200:
            answer = response.json()["answer"]
            chat_history.append((user_input, answer))
        else:
            st.error("Something went wrong!")

# Display chat history
for q, a in reversed(chat_history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a['generations'][0][0]['text'].strip()}")
