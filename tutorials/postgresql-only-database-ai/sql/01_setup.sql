-- 01_setup.sql
-- Enable pgvector and create the documents table with an HNSW index.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id          BIGSERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    metadata    JSONB,
    embedding   vector(1536)
);

-- HNSW index for fast approximate nearest neighbor search.
-- vector_cosine_ops tells PostgreSQL to use cosine distance.
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
