-- Run this in your Supabase SQL Editor
-- 1. Enable pgvector extension
create extension if not exists vector;

-- Drop existing resources since we are changing embedding dimensions
drop table if exists documents cascade;
drop function if exists match_documents;

-- 2. Create the table for your documents
create table if not exists documents (
  id uuid primary key default gen_random_uuid(),
  content text, 
  metadata jsonb, 
  embedding vector(384) -- all-MiniLM-L6-v2 uses 384 dimensions
);

-- 3. Create the missing 'match_documents' function
create or replace function match_documents (
  query_embedding vector(384),
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding;
end;
$$;
