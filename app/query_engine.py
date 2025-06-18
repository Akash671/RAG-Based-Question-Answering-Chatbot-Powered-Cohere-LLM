# query_engine.py

from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

def embed_query(query: str, model=None):
    model = model or SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(query).tolist()

def retrieve_relevant_chunks(chroma_collection, query: str, k: int = 5):
    query_vector = embed_query(query)
    results = chroma_collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas"]
    )
    
    relevant_chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        relevant_chunks.append({
            "text": doc,
            "metadata": meta
        })

    return relevant_chunks

def build_prompt(query: str, chunks: list):
    context = "\n\n".join([chunk["text"] for chunk in chunks])
    return f"""Answer the following question using the context below:

Question: {query}

Context:
{context}

Answer:"""
