-- 1. Ensure pgvector is enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create a separate table for Gemini embeddings
CREATE TABLE IF NOT EXISTS public.documents_gemini (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT,
    metadata JSONB,
    embedding VECTOR(768)
);

-- 3. Create the RPC function used by your Python code
CREATE OR REPLACE FUNCTION public.match_documents_gemini(
    query_embedding VECTOR(768),
    filter JSONB DEFAULT '{}'::JSONB
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE SQL
AS $$
    SELECT
        d.id,
        d.content,
        d.metadata,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM public.documents_gemini AS d
    WHERE d.metadata @> filter
    ORDER BY d.embedding <=> query_embedding;
$$;

-- 4. Refresh Supabase's API schema cache
NOTIFY pgrst, 'reload schema';