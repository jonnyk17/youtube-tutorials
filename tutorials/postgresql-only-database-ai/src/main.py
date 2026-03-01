"""RAG chatbot using PostgreSQL with pgvector for hybrid search."""

import os
from pathlib import Path

import psycopg
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)
EMBEDDING_MODEL = "text-embedding-ada-002"

client = OpenAI()

app = FastAPI()


def get_db():
    """Return a new database connection."""
    return psycopg.connect(DATABASE_URL)


def get_embedding(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def hybrid_search(conn, query: str, limit: int = 5) -> list[dict]:
    """Search documents using hybrid search (vector + full-text with RRF)."""
    embedding = get_embedding(query)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content, rrf_score FROM hybrid_search(%s, %s::vector, %s)",
            (query, str(embedding), limit),
        )
        return [
            {"id": row[0], "content": row[1], "score": row[2]}
            for row in cur.fetchall()
        ]


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the chat UI."""
    html_path = Path(__file__).parent / "static" / "index.html"
    return html_path.read_text()


@app.post("/chat")
async def chat(request: ChatRequest):
    """Retrieve relevant documents and stream an LLM response."""
    conn = get_db()
    try:
        results = hybrid_search(conn, request.message)
        context = "\n\n".join(
            f"[Document {r['id']}]: {r['content']}" for r in results
        )

        def generate():
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. Answer the user's question "
                            "based on the following documents. If the documents don't "
                            "contain relevant information, say so.\n\n"
                            f"Documents:\n{context}"
                        ),
                    },
                    {"role": "user", "content": request.message},
                ],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return StreamingResponse(generate(), media_type="text/plain")
    finally:
        conn.close()
