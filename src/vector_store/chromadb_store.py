import dspy
import chromadb
from pathlib import Path
from src.vector_store.base import AbstractRetriever
from src.vector_store.dummy import DUMMY_DOCUMENTS

class ChromaRetriever(AbstractRetriever):
    """
    Production-ready Retriever using ChromaDB for true vector similarity search.
    """
    def __init__(self, collection_name="agentic_docs", k=3):
        self.k = k
        persist_dir = str(Path.cwd() / "chroma_db")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
        # Auto-seed if empty for an out-of-the-box experience
        if self.collection.count() == 0:
            print("ChromaDB collection is empty. Seeding with default documents...")
            self.collection.add(
                documents=DUMMY_DOCUMENTS,
                ids=[f"doc_{i}" for i in range(len(DUMMY_DOCUMENTS))]
            )
            print("Seeding complete.")

    def forward(self, query_or_queries, k=None, **kwargs):
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        k = k if k is not None else self.k
        
        results = []
        for query in queries:
            # Query ChromaDB (which uses a default sentence-transformers embedding model under the hood)
            query_results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            if query_results and "documents" in query_results and query_results["documents"]:
                docs = query_results["documents"][0]
                results.extend([dspy.Prediction(long_text=doc) for doc in docs])
                
        return results
