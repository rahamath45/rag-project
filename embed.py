import ollama
from chunk_text import chunks

embeddings = []

for i, chunk in enumerate(chunks):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )

    embeddings.append(response["embedding"])

    if (i + 1) % 500 == 0:
        print(f"Done {i+1}/{len(chunks)}")

print("Total embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))