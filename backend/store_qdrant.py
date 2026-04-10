import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import requests
from chunk_text import chunks, chunk_metadata   # we will use metadata

client = QdrantClient(host="localhost", port=6333)


if not client.collection_exists("ncert"):
    client.create_collection(
        collection_name="ncert",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    print("Created collection 'ncert'")
else:
    print("Collection 'ncert' already exists")

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return response.json()["embedding"]


BATCH_SIZE = 100

for batch_start in range(0, len(chunks), BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, len(chunks))

    points = []

    for i in range(batch_start, batch_end):
        chunk = chunks[i]
        metadata = chunk_metadata[i]   # contains class

        vector = get_embedding(chunk)

        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "text": chunk,
                "class": metadata["class"]
            }
        })

    client.upsert(
        collection_name="ncert",
        points=points
    )

    print(f"Stored batch {batch_start}-{batch_end}")

print("✅ Stored with class metadata")