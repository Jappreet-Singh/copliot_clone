from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)
