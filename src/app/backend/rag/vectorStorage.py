import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# We need the service role key to insert documents into Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Hugging Face embeddings require HUGGINGFACEHUB_API_TOKEN to be set in environment
    hf_api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    
    if not hf_api_key:
        print("Warning: HUGGINGFACEHUB_API_TOKEN not set. Embeddings will fail.")
        
    embedding = HuggingFaceInferenceAPIEmbeddings(
        api_key=hf_api_key, 
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # ---------------------------------------------------------
    # MONKEY PATCH: Fix for LangChain Supabase param bug
    # ---------------------------------------------------------
    from typing import List, Tuple, Dict, Any, Optional
    from langchain_core.documents import Document
    
    def _patched_search(self, query: List[float], k: int, filter: Optional[Dict[str, Any]] = None, postgrest_filter: Optional[str] = None, score_threshold: Optional[float] = None) -> List[Tuple[Document, float]]:
        match_params = self.match_args(query, filter)
        builder = self._client.rpc(self.query_name, match_params)
        builder = builder.limit(k)  # Fix: Use builder method directly instead of .params
        res = builder.execute()
        return [(Document(metadata=s.get("metadata", {}), page_content=s.get("content", "")), s.get("similarity", 0.0)) for s in res.data if s.get("content")]

    SupabaseVectorStore.similarity_search_by_vector_with_relevance_scores = _patched_search
    # ---------------------------------------------------------
    
    vector_db = SupabaseVectorStore(
        client=supabase,
        embedding=embedding,
        table_name="documents",
        query_name="match_documents"
    )
else:
    print("Warning: Supabase keys not set. Vector DB operations will fail.")
    vector_db = None
