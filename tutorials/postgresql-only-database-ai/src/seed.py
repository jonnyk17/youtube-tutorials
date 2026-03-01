"""Seed the documents table with sample data and real embeddings."""

import json
import os

import psycopg
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)
EMBEDDING_MODEL = "text-embedding-3-small"

client = OpenAI()

DOCUMENTS = [
    {
        "content": (
            "pgvector is a PostgreSQL extension that adds support for vector "
            "similarity search. It allows you to store embeddings as a native "
            "column type and query them using distance operators like cosine "
            "distance, inner product, and L2 distance."
        ),
        "metadata": {"source": "pgvector-docs", "topic": "overview"},
    },
    {
        "content": (
            "HNSW (Hierarchical Navigable Small World) is an approximate nearest "
            "neighbor algorithm. In pgvector, you create an HNSW index with "
            "CREATE INDEX USING hnsw. It provides fast query times with high "
            "recall, making it suitable for production workloads."
        ),
        "metadata": {"source": "pgvector-docs", "topic": "indexing"},
    },
    {
        "content": (
            "Cosine distance measures the angle between two vectors, ignoring "
            "magnitude. In PostgreSQL with pgvector, the cosine distance operator "
            "is <=>. A cosine distance of 0 means identical direction, while 2 "
            "means opposite direction."
        ),
        "metadata": {"source": "pgvector-docs", "topic": "distance-metrics"},
    },
    {
        "content": (
            "RAG (Retrieval-Augmented Generation) is a technique where you "
            "retrieve relevant documents from a database and pass them as context "
            "to a large language model. This grounds the LLM response in your "
            "actual data instead of relying solely on its training data."
        ),
        "metadata": {"source": "ai-engineering", "topic": "rag"},
    },
    {
        "content": (
            "Full-text search in PostgreSQL uses tsvector for indexed document "
            "representations and tsquery for search queries. The @@ operator "
            "matches a tsquery against a tsvector. Combined with GIN indexes, "
            "full-text search is fast even on large tables."
        ),
        "metadata": {"source": "postgresql-docs", "topic": "full-text-search"},
    },
    {
        "content": (
            "Hybrid search combines vector similarity search with keyword-based "
            "full-text search. Reciprocal Rank Fusion (RRF) merges ranked results "
            "from both methods. Documents scoring well in both lists rise to the "
            "top, improving retrieval quality over either method alone."
        ),
        "metadata": {"source": "ai-engineering", "topic": "hybrid-search"},
    },
    {
        "content": (
            "The text-embedding-3-small model from OpenAI produces "
            "1536-dimensional vectors. These embeddings capture semantic meaning, "
            "so similar concepts have similar vector representations regardless "
            "of the exact words used."
        ),
        "metadata": {"source": "openai-docs", "topic": "embeddings"},
    },
    {
        "content": (
            "PostgreSQL has been in production for over 35 years. It supports "
            "ACID transactions, JSONB for semi-structured data, full-text search, "
            "and with pgvector, dense vector embeddings. This makes it a unified "
            "data platform for AI applications."
        ),
        "metadata": {"source": "postgresql-docs", "topic": "overview"},
    },
    {
        "content": (
            "IVFFlat is an older indexing method in pgvector that partitions "
            "vectors into lists using k-means clustering at index build time. "
            "While it uses less memory than HNSW, data must exist in the table "
            "before the index is created, and it generally provides lower recall. "
            "HNSW is recommended for most production use cases."
        ),
        "metadata": {"source": "pgvector-docs", "topic": "indexing"},
    },
    {
        "content": (
            "Supabase provides hosted PostgreSQL with pgvector pre-installed. "
            "All standard pgvector SQL works on Supabase without modification. "
            "This gives you a managed vector database without running your own "
            "infrastructure."
        ),
        "metadata": {"source": "supabase-docs", "topic": "vector-search"},
    },
]


def get_embedding(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def seed():
    """Embed all documents and insert them into PostgreSQL."""
    conn = psycopg.connect(DATABASE_URL)

    # Generate embeddings for all documents in one batch
    texts = [doc["content"] for doc in DOCUMENTS]
    print(f"Generating embeddings for {len(texts)} documents...")
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    embeddings = [item.embedding for item in response.data]

    with conn.cursor() as cur:
        # Clear existing data
        cur.execute("DELETE FROM documents")

        for doc, embedding in zip(DOCUMENTS, embeddings):
            cur.execute(
                """
                INSERT INTO documents (content, metadata, embedding)
                VALUES (%s, %s::jsonb, %s::vector)
                """,
                (doc["content"], json.dumps(doc["metadata"]), str(embedding)),
            )

        conn.commit()

    conn.close()
    print(f"Seeded {len(DOCUMENTS)} documents with embeddings.")


if __name__ == "__main__":
    seed()
