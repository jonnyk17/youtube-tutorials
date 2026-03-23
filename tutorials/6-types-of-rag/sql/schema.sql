-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Products table (structured data for SQL RAG)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    color TEXT NOT NULL,
    description TEXT NOT NULL,
    -- Full-text search index column
    description_tsv TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', description)) STORED,
    -- Vector embedding column (OpenAI text-embedding-3-small outputs 1536 dimensions)
    embedding VECTOR(1536)
);

-- Full-text search index
CREATE INDEX idx_products_fts ON products USING GIN (description_tsv);

-- Vector similarity search index (cosine distance)
CREATE INDEX idx_products_embedding ON products USING hnsw (embedding vector_cosine_ops);

-- Document chunks table (for chunked policy docs)
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_tsv TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
    embedding VECTOR(1536)
);

CREATE INDEX idx_chunks_fts ON document_chunks USING GIN (content_tsv);
CREATE INDEX idx_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);
