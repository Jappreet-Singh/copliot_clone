from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorStorage import vector_db

# modified phase 3 upload ingestion code
# Ingests text into the vector database
def ingest_text(text: str, source: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    vector_db.add_texts(
        texts=chunks,
        metadatas=[{"source": source} for _ in chunks]
    )

    vector_db.persist()