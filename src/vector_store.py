import os
import chromadb
from chromadb.utils import embedding_functions

# Mock Dataset
FACTS = [
    "Project Orion was launched in 2023 to revolutionize cloud storage.",
    "The CEO of Project Orion is Dr. Amelia Vance.",
    "Project Orion's main backend framework is FastAPI.",
    "The Orion database uses Qdrant for vector search, though some teams use ChromaDB.",
    "Orion's frontend is built entirely in React.",
    "The primary security vulnerability patched in 2024 was a cross-site scripting flaw in the auth module.",
    "Project Orion raised $50 million in Series B funding.",
    "The headquarters of Project Orion is in Austin, Texas.",
    "Orion employs a strictly serverless architecture on AWS.",
    "The next major release of Orion is scheduled for Q4 2026."
]

def get_chroma_collection():
    """Initializes and populates an in-memory ChromaDB for testing."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="orion_docs",
        # Using default sentence-transformers embedding function
    )
    
    # Populate only if empty
    if collection.count() == 0:
        print("Ingesting mock facts into vector database...")
        collection.add(
            documents=FACTS,
            metadatas=[{"source": "wiki"} for _ in FACTS],
            ids=[f"fact_{i}" for i in range(len(FACTS))]
        )
        
    return collection

def retrieve(query: str, k: int = 2) -> list[str]:
    """Retrieves top-k relevant documents from the vector store."""
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    # Return the raw string documents
    return results["documents"][0] if results["documents"] else []

if __name__ == "__main__":
    col = get_chroma_collection()
    print(f"Collection count: {col.count()}")
    print("Test retrieval for 'Who is the CEO?':", retrieve("Who is the CEO?"))
