from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from embed import embeddings
from chunk_text import chunks

# connect
client = QdrantClient(host="localhost", port=6333)

# create collection
client.recreate_collection(
    collection_name="ncert",
    vectors_config=VectorParams(
        size=len(embeddings[0]),
        distance=Distance.COSINE
    )
)

points = []

for i in range(len(chunks)):
    points.append(
        PointStruct(
            id=i,
            vector=embeddings[i],
            payload={"text": chunks[i]}
        )
    )

# upload
client.upsert(
    collection_name="ncert",
    points=points
)

print("✅ Stored in Qdrant")