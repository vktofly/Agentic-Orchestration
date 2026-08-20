import os
from src.vector_store.base import AbstractRetriever
from src.vector_store.dummy import DummyRetriever
from src.vector_store.chromadb_store import ChromaRetriever

def get_retriever(k: int = 3) -> AbstractRetriever:
    """
    Factory function to instantiate the correct retriever based on the 
    VECTOR_STORE_TYPE environment variable.
    """
    store_type = os.getenv("VECTOR_STORE_TYPE", "dummy").lower()
    
    if store_type == "chromadb":
        print(f"Using Vector Store: ChromaDB (k={k})")
        return ChromaRetriever(k=k)
    else:
        print(f"Using Vector Store: Dummy Keyword Matcher (k={k})")
        return DummyRetriever(k=k)
