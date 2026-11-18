import os

from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client, Client
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# We need the service role key to insert documents into Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")


supabase: Client = create_client(supabase_url, supabase_key)


google_api_key = os.environ.get("GOOGLE_API_KEY")

if not google_api_key:
    raise RuntimeError("Missing GOOGLE_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=google_api_key,
    output_dimensionality=768
)

# testing the embedding to ensure it works
try:
    test_embedding = embedding.embed_query(
        "Testing Gemini embeddings"
    )

    logger.info(
        "Gemini embedding successful. Dimensions: %d",
        len(test_embedding)
    )

except Exception:
    logger.exception("Gemini embedding test failed")
    raise

    
    # ---------------------------------------------------------
    # MONKEY PATCH: Fix for LangChain Supabase param bug
    # ---------------------------------------------------------
from typing import List, Tuple, Dict, Any, Optional
from langchain_core.documents import Document
    
    
def _patched_search(
    self,
    query: List[float],
    k: int,
    filter: Optional[Dict[str, Any]] = None,
    postgrest_filter: Optional[str] = None,
    score_threshold: Optional[float] = None
) -> List[Tuple[Document, float]]:

    logger.info("RAG: Building Supabase RPC parameters")

    match_params = self.match_args(query, filter)

    # LOG 1: Check parameter names, not sensitive values
    logger.info("RAG: RPC parameter keys: %s", list(match_params.keys()))

    builder = self._client.rpc(self.query_name, match_params)

    # LOG 2: Confirm RPC execution starts
    logger.info("RAG: Executing Supabase RPC: %s", self.query_name)

    builder = builder.limit(k)

    res = builder.execute()
    logger.info("RAG RPC response type: %s", type(res))
    logger.info("RAG RPC data type: %s", type(res.data))

    if res.data:
        logger.info(
            "RAG RPC first row keys: %s",
            list(res.data[0].keys())
        )
    
    # LOG 3: Check returned rows
    logger.info("RAG: Supabase returned %d rows", len(res.data))

    # LOG 4: Inspect returned column names
    if res.data:
        logger.info("RAG: Supabase returned columns: %s", list(res.data[0].keys()))

    return [
        (
            Document(
                metadata=s.get("metadata", {}),
                page_content=s.get("content", "")
            ),
            s.get("similarity", 0.0)
        )
        for s in res.data if s.get("content")
    ]
    
SupabaseVectorStore.similarity_search_by_vector_with_relevance_scores = (
    _patched_search
)
    
vector_db = SupabaseVectorStore(
    client=supabase,
    embedding=embedding,
    table_name="documents_gemini",
    query_name="match_documents_gemini"
)

logger.info("RAG: Supabase vector store initialized successfully")
