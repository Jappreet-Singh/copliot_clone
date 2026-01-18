from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorStorage import vector_db
from langchain_core.documents import Document

# modified phase 3 upload ingestion code
# Ingests text into the vector database
def ingest_text(text: str, source: str):
    
    if not text or not text.strip():
        raise ValueError("Text for ingestion is empty")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)
    
    if not chunks:
        raise ValueError("No text chunks were created from the provided text")

    docs = [
        Document(page_content=chunk, metadata={"source": source})
        for chunk in chunks
    ]
    try:
        vector_db.add_documents(docs)
        print(f"Successfully ingested {len(docs)} documents from source: {source}")
    except Exception as e:
        raise RuntimeError(f"Failed to ingest documents: {e}") from e