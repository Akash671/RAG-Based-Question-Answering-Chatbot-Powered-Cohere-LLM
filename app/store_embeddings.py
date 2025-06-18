# store_embeddings.py (updated for new Chroma API)

import chromadb
from chromadb.config import Settings

def store_in_chromadb(embeddings, metadata, collection_name="documents"):
    #  Use new Client initialization (no Settings required for default local usage)
    client = chromadb.PersistentClient(path=".chromadb")  # <- NEW way

    if collection_name in [col.name for col in client.list_collections()]:
        client.delete_collection(name=collection_name)

    collection = client.create_collection(name=collection_name)

    for i, meta in enumerate(metadata):
        uid = f"{meta['doc_id']}_{meta['chunk_index']}"
        collection.add(
            ids=[uid],
            documents=[meta["text"]],
            metadatas=[meta],
            embeddings=[embeddings[i].tolist()]
        )

    return client, collection
