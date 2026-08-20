import dspy
from src.vector_store.base import AbstractRetriever

DUMMY_DOCUMENTS = [
    "DSPy is a framework for algorithmically optimizing LM prompts and weights.",
    "LangGraph is a library for building stateful, multi-actor applications with LLMs.",
    "Qdrant is a vector similarity search engine and vector database.",
    "Retrieval-Augmented Generation (RAG) grounds LLM outputs in retrieved factual context.",
    "The BootstrapFewShot teleprompter in DSPy optimizes prompt instructions and examples.",
    "LLM-as-a-judge uses an LLM to evaluate the quality of another LLM's output.",
    "G-Eval is a framework for using LLMs to grade text generation.",
    "Agentic workflows allow LLMs to reflect, route, and loop until a condition is met.",
]

class DummyRetriever(AbstractRetriever):
    """
    Dummy Retriver using naive keyword overlap matching for fast local testing.
    """
    def __init__(self, k=3):
        self.k = k

    def forward(self, query_or_queries, k=None, **kwargs):
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        k = k if k is not None else self.k
        
        results = []
        for query in queries:
            query_words = set(query.lower().split())
            
            def score(doc):
                doc_words = set(doc.lower().split())
                return len(query_words.intersection(doc_words))
                
            sorted_docs = sorted(DUMMY_DOCUMENTS, key=score, reverse=True)
            results.extend([dspy.Prediction(long_text=doc) for doc in sorted_docs[:k]])
            
        return results
