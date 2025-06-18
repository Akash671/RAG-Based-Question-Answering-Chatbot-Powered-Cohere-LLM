# api.py

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extract_documents import extract_documents
from preprocess_documents import preprocess_text
from create_embeddings import chunk_and_embed
from store_embeddings import store_in_chromadb
from query_engine import retrieve_relevant_chunks, build_prompt
import uvicorn
from langchain.llms import cohere
from dotenv import load_dotenv



# Load variables from .env
load_dotenv()

# Get key from environment
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("❌ COHERE_API_KEY environment variable not found!")

# Initialize Cohere
llm = cohere.Cohere(cohere_api_key=api_key, temperature=0.1)


# Set up FastAPI
app = FastAPI(title="RAG-powered Chatbot (Cohere)")

class QueryRequest(BaseModel):
    question: str

# 🧠 Function to call Cohere using your exact style
def call_cohere(prompt_text: str) -> str:
    response = llm.generate(
        prompts=[prompt_text],
        max_tokens=300,
        temperature=0.5
    )
    return response #.generations[0].strip()

# 🔄 Document preprocessing + embedding
print("🔍 Extracting documents and initializing vector store...")

raw_docs, doc_meta = extract_documents()
if not raw_docs:
    raise ValueError("❌ No documents found in the input folder.")

preprocessed_docs = {doc_id: preprocess_text(text) for doc_id, text in raw_docs.items()}
embeddings, embedding_meta = chunk_and_embed(preprocessed_docs)
_, chroma_collection = store_in_chromadb(embeddings, embedding_meta)

print("✅ Vector database initialized with embedded content.")

# 🔗 Endpoint: Ask
@app.post("/ask")
def ask_question(payload: QueryRequest):
    try:
        top_chunks = retrieve_relevant_chunks(chroma_collection, payload.question, k=5)
        prompt = build_prompt(payload.question, top_chunks)
        answer = call_cohere(prompt)

        return {
            "question": payload.question,
            "answer": answer,
            "context_used": [chunk["text"] for chunk in top_chunks]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cohere LLM failed: {str(e)}")

# Optional CLI run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
