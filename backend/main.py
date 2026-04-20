from fastapi import FastAPI
import os
from langfuse import Langfuse, observe
from fastapi.middleware.cors import CORSMiddleware
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge import Knowledge
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.document import Document
from agno.vectordb.qdrant import Qdrant
from agno.vectordb.search import SearchType

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

# Load system prompt
def load_prompt():
    with open("prompts/system_prompt.txt", "r") as f:
        return f.read()

# Setup Agno-native vector DB with Ollama embedder
vector_db = Qdrant(
    collection="ncert",
    embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768),
    url="http://localhost:6333",
    search_type=SearchType.vector,
    distance="cosine",
)

# Setup Agno-native Knowledge base
knowledge = Knowledge(
    name="ncert_knowledge",
    vector_db=vector_db,
)

# Create Agent with native RAG
rag_agent = Agent(
    name="NCERT RAG",
    model=Ollama(id="llama3:latest"),
    knowledge=knowledge,
    search_knowledge=False,
    add_knowledge_to_context=True,
    instructions=load_prompt(),
    markdown=True,
)

@app.get("/ask")
def ask(question: str, class_name: str = None):
    try:
        with langfuse.start_as_current_observation(
            name="rag-query",
            input={"question": question}
        ) as trace:
            # Set knowledge filter if class_name provided
            if class_name:
                rag_agent.knowledge_filters = {"class": class_name}

            response = rag_agent.run(question)

            trace.update(output={"answer": response.content})

            return {
                "question": question,
                "answer": response.content,
                "class": class_name
            }

    except Exception as e:
        return {"error": str(e)}
