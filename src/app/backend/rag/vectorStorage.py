import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
    
    # Gemini embeddings require GOOGLE_API_KEY to be set in environment
    embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_db = SupabaseVectorStore(
        client=supabase,
        embedding=embedding,
        table_name="documents",
        query_name="match_documents"
    )
else:
    print("Warning: Supabase keys not set. Vector DB operations will fail.")
    vector_db = None
