-- 02_vector_search.sql
-- Vector similarity search using cosine distance.
-- $1 is the query embedding (a 1536-dimensional vector).

SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 5;
