from rag.vectorStorage import vector_db
import logging

logger = logging.getLogger(__name__)

def retrieve_context(query: str, k: int = 3) -> str:
    try:
        logger.info("RAG: Starting similarity search")

        docs = vector_db.similarity_search(query, k=k)

        logger.info("RAG: Similarity search returned %d documents", len(docs))

        if not docs:
            return ""

        return "\n\n".join(doc.page_content for doc in docs)

    except Exception:
        logger.exception("RAG QUERY ERROR")
        raise