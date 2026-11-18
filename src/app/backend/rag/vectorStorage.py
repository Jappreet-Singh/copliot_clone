import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client, Client
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

vector_db = None
embedding = None

# We need the service role key to insert documents into Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
hf_api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

if not supabase_url or not supabase_key:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")

if not hf_api_key:
    raise RuntimeError("Missing HUGGINGFACEHUB_API_TOKEN")

supabase: Client = create_client(supabase_url, supabase_key)

embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=hf_api_key,
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    api_url=(
        "https://router.huggingface.co/hf-inference/models/"
        "sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
    )
)

    
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
        logger.info("RAG RPC first row: %s", res.data[0])
    
    
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
    
vector_db = SupabaseVectorStore(
    client=supabase,
    embedding=embedding,
    table_name="documents",
    query_name="match_documents"
)

logger.info("RAG: Supabase vector store initialized successfully")
