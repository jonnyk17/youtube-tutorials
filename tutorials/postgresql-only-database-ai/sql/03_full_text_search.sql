-- 03_full_text_search.sql
-- Add a generated tsvector column and GIN index for full-text search.

ALTER TABLE documents
ADD COLUMN fts tsvector
    GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;

CREATE INDEX ON documents USING gin(fts);

-- Full-text search query using websearch_to_tsquery.
SELECT id, content
FROM documents
WHERE fts @@ websearch_to_tsquery('english', 'your search term here')
ORDER BY ts_rank(fts, websearch_to_tsquery('english', 'your search term here')) DESC
LIMIT 5;
