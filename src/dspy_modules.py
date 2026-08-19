import os
import dspy
from src.vector_store import retrieve

def setup_dspy():
    """Initializes the DSPy framework with the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. DSPy requires this to compile and execute prompts.")

    # Configure DSPy to use Gemini
    # Note: DSPy uses google-generativeai under the hood for dspy.Google
    gemini = dspy.Google(model="gemini-1.5-flash", api_key=api_key)
    
    # Set the global DSPy settings
    dspy.settings.configure(lm=gemini)
    return gemini

# ----------------------------------------------------
# DSPy Signatures and Modules
# ----------------------------------------------------

class GenerateAnswer(dspy.Signature):
    """Answer questions based strictly on the retrieved context."""
    context = dspy.InputField(desc="Information retrieved from the vector database")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="A concise, factual answer. If the context doesn't contain the answer, say 'I don't know.'")

class GradeAnswer(dspy.Signature):
    """Evaluate whether an answer correctly addresses the question using the given context."""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.InputField()
    is_correct = dspy.OutputField(desc="Return strictly 'True' if correct, or 'False' if incorrect or hallucinated.")

class RAGGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        # Use ChainOfThought instead of a raw Predict for better reasoning
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question, context):
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(answer=prediction.answer)

class RAGGrader(dspy.Module):
    def __init__(self):
        super().__init__()
        self.grade = dspy.Predict(GradeAnswer)
        
    def forward(self, question, context, answer):
        result = self.grade(context=context, question=question, answer=answer)
        return dspy.Prediction(is_correct=result.is_correct)
