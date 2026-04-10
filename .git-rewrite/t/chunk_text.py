from load_pdf import documents

CHUNK_SIZE = 500
OVERLAP = 50

chunks = []
chunk_metadata = []

for doc in documents:
    text = doc["text"]
    class_name = doc["class"]

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(chunk)

        chunk_metadata.append({
            "class": class_name
        })

        start += CHUNK_SIZE - OVERLAP


print("Total chunks:", len(chunks))
print("First chunk:", chunks[0])