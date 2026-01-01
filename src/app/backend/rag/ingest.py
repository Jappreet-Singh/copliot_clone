from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorStorage import vector_db
from langchain_core.documents import Document

# modified phase 3 upload ingestion code
# Ingests text into the vector database
def ingest_text(text: str, source: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    docs = [
        Document(page_content=chunk, metadata={"source": source})
        for chunk in chunks
    ]

    vector_db.add_documents(docs)
