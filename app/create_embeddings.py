# create_embeddings.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_and_embed(doc_data: dict, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )

    embeddings = []
    metadata = []

    for doc_id, text in doc_data.items():
        chunks = text_splitter.split_text(text)

        for idx, chunk in enumerate(chunks):
            vector = embedding_model.encode(chunk)
            embeddings.append(vector)
            metadata.append({
                "doc_id": doc_id,
                "chunk_index": idx,
                "text": chunk
            })

    return np.array(embeddings).astype("float32"), metadata
