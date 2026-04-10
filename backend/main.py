from fastapi import FastAPI
from qdrant_client import QdrantClient
import requests
import os
from langfuse import Langfuse, observe
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# connect qdrant
client = QdrantClient(host="qdrant", port=6333)


def get_embedding(text):
    response = requests.post(
        "http://host.docker.internal:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    if "embedding" not in data:
        return {"error": data}

    return data["embedding"]


@observe()
def hybrid_search(question, class_name=None):
    query_vector = get_embedding(question)

    filter_query = None

    if class_name:
        filter_query = {
            "must": [
                {
                    "key": "class",
                    "match": {"value": class_name}
                }
            ]
        }

    results = client.query_points(
        collection_name="ncert",
        query=query_vector,
        query_filter=filter_query,
        limit=5
    )

    return results.points

# ✅ Reranking
@observe()
def rerank(question, results):
    scored = []

    for r in results:
        text = r.payload.get("text", "")
        score = len(set(question.lower().split()) & set(text.lower().split()))
        scored.append((score, text))

    scored.sort(reverse=True)

    return [text for _, text in scored[:3]]

@app.get("/ask")
def ask(question: str, class_name:str = None):
    try:
        with langfuse.start_as_current_observation(
            name="rag-query",
            input={"question": question}
        ) as trace:
            # hybrid search
            results = hybrid_search(question)

            if not results:
                return {"error": "No data found in Qdrant"}

            # rerank
            top_chunks = rerank(question, results)

            context = " ".join(top_chunks)

            prompt = f"""
Answer the question based on context.

Context:
{context}

Question:
{question}
"""

            response = requests.post(
                "http://host.docker.internal:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )

            answer = response.json().get("response", "No response")

            trace.update(
                output={"answer": answer}
            )

        return {
            "question": question,
            "answer": answer,
            "class": class_name
        }

    except Exception as e:
        return {"error": str(e)}