import os
import dspy
from dspy.teleprompt import BootstrapFewShot

# ==============================================================================
# 1. DSPy Signature: Declares the input/output contract for the LLM
# ==============================================================================
# Instead of writing a manual prompt ("You are an expert..."), we define what inputs
# the model receives and what output it must produce. DSPy compiles the exact wording.
class GenerateAnswer(dspy.Signature):
    """Answer questions with short, precise, factual answers based on the context."""
    context = dspy.InputField(desc="Factual context retrieved from a database")
    question = dspy.InputField(desc="The user's question")
    answer = dspy.OutputField(desc="A precise, accurate answer")


# ==============================================================================
# 2. DSPy Module: Encapsulates the RAG Pipeline logic
# ==============================================================================
# Combines retrieval and prediction into a callable, optimizable pipeline.
class RAGModule(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        # self.retrieve calls the configured Retrieval Model (RM) to get top-k passages
        self.retrieve = dspy.Retrieve(k=num_passages)
        # self.generate_answer uses the signature defined above to query the LLM
        self.generate_answer = dspy.Predict(GenerateAnswer)

    def forward(self, question):
        # Step A: Query vector store for relevant context passages
        context = self.retrieve(question).passages
        # Step B: Feed context + user question into the LLM predictor
        prediction = self.generate_answer(context=context, question=question)
        
        # Step C: Return structured DSPy prediction object containing context & answer
        return dspy.Prediction(context=context, answer=prediction.answer)


# ==============================================================================
# 3. Training Set for Prompt Optimization
# ==============================================================================
# DSPy will use these ground-truth examples to bootstrap and select high-performing
# few-shot demonstrations automatically.
TRAINING_SET = [
    dspy.Example(question="What is DSPy?", answer="A framework for algorithmically optimizing LM prompts and weights.").with_inputs("question"),
    dspy.Example(question="How does G-Eval work?", answer="It uses an LLM to evaluate the quality of text generation.").with_inputs("question"),
    dspy.Example(question="What is the purpose of LangGraph?", answer="Building stateful, multi-actor applications with LLMs.").with_inputs("question")
]


# ==============================================================================
# 4. Evaluation Metric for Optimization
# ==============================================================================
# Measures whether a generated answer satisfies the required standard during compilation.
def answer_exact_match(example, pred, trace=None):
    # Returns True if the expected answer key phrase is present in the prediction
    return example.answer.lower() in pred.answer.lower()


# ==============================================================================
# 5. Compilation & Caching Function
# ==============================================================================
# Compiles the RAG module using BootstrapFewShot or loads a pre-compiled JSON cache
# to avoid expensive LLM calls on every server startup.
def compile_rag_module(cache_file="compiled_rag.json", auto_compile=False):
    rag = RAGModule(num_passages=2)
    cache_path = os.path.join(os.path.dirname(__file__), cache_file)
    
    # Check if we have an already-compiled module on disk
    if os.path.exists(cache_path):
        try:
            print(f"Loading cached compiled DSPy module from {cache_path}...")
            rag.generate_answer.load(cache_path)
            print("Loaded cached DSPy module successfully.")
            return rag
        except Exception as e:
            print(f"Failed to load cached module: {e}")
            
    if not auto_compile:
        print("Note: Returning uncompiled DSPy RAG Module (auto_compile=False).")
        return rag
            
    print("Compiling DSPy RAG Module (optimizing prompts)...")
    try:
        # BootstrapFewShot simulates runs, evaluates traces via the metric, and picks best demos
        teleprompter = BootstrapFewShot(metric=answer_exact_match, max_bootstrapped_demos=2, max_labeled_demos=2)
        compiled_rag = teleprompter.compile(rag, trainset=TRAINING_SET)
        print("Compilation complete.")
        
        # Cache the compiled weights/prompts to disk for future runs
        try:
            compiled_rag.generate_answer.save(cache_path)
        except Exception as e:
            print(f"Note: Could not save compiled module cache: {e}")
        return compiled_rag
    except Exception as e:
        print(f"Warning: Prompt compilation failed ({e}). Falling back to uncompiled RAG module.")
        return rag
