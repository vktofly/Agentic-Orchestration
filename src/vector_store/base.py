from abc import ABC, abstractmethod

class AbstractRetriever(ABC):
    """
    Abstract base class for DSPy Retrieval Models (RMs).
    Enforces the DSPy RM protocol.
    """
    
    @abstractmethod
    def forward(self, query_or_queries, k=None, **kwargs):
        """
        Retrieves top-k documents for the given query.
        Must return a list of dspy.Prediction(long_text=...) objects.
        """
        pass

    def __call__(self, query_or_queries, k=None, **kwargs):
        """
        Enables instances to be called directly, as expected by DSPy.
        """
        return self.forward(query_or_queries, k=k, **kwargs)
