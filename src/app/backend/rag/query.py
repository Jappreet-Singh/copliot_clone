from rag.vectorStorage import vector_db

def retrieve_context(query: str, k: int = 3 ) -> str:
    docs = vector_db.similarity_search(query, k=k)

    if not docs:
        return ""
    
    return "\n\n".join([doc.page_content for doc in docs])