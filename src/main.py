import os
import dspy
from dotenv import load_dotenv
from pathlib import Path
from src.vector_store.qdrant_store import QdrantDSPyRM
from src.dspy_modules.qa_system import compile_rag_module
from src.graph.orchestrator import build_agent_graph
from src.dspy_modules.model_factory import get_model

# ==============================================================================
# CLI Entrypoint for Testing the Agentic Pipeline Locally
# ==============================================================================
def main():
    # 1. Load environment variables (.env.local in project root)
    env_path = Path(__file__).resolve().parents[1] / ".env.local"
    load_dotenv(dotenv_path=env_path)
    
    print("\n--- 1. Setting up Qdrant Vector Store ---")
    # Initialize the retrieval adapter and bind it globally in DSPy
    rm = QdrantDSPyRM()
    dspy.settings.configure(rm=rm)
    
    print("\n--- 2. Optimizing Prompts via DSPy ---")
    # Load cached prompt optimization file or compile a new one
    compiled_rag = compile_rag_module()
    
    print("\n--- 3. Building LangGraph Orchestrator ---")
    # Assemble the state machine with retriever + compiled generator + grader
    retriever = dspy.Retrieve(k=2)
    agent = build_agent_graph(compiled_rag, retriever)
    
    print("\n--- 4. Initializing Provider (Gemini) ---")
    try:
        model = get_model("gemini")
        print("Model initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        return
        
    print("\n--- 5. Running Agent Workflow ---")
    # Test Question to evaluate the workflow
    question = "How do agentic workflows work?"
    print(f"\nUser Query: {question}\n")
    
    # Define initial input state
    initial_state = {
        "question": question,
        "context": None,
        "answer": None,
        "retries": 0,
        "is_valid": False
    }
    
    # Stream the graph execution step-by-step
    # We use a context manager to inject the LLM solely for this execution
    with dspy.context(lm=model):
        for output in agent.stream(initial_state):
            # LangGraph yields state at each node boundary (retrieve -> generate -> grade)
            for key, value in output.items():
                pass # The nodes print their own live trace information
                
        # Invoke the graph to fetch the final completed state
        final_state = agent.invoke(initial_state)
    
    print("\n--- Final Output ---")
    print(f"Verified Answer: {final_state['answer']}")
    print(f"Total Generation Retries: {final_state['retries']}")

if __name__ == "__main__":
    main()
