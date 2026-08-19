import os
import dspy
from src.dspy_modules import setup_dspy
from src.graph import build_graph

def main():
    print("="*50)
    print("Agentic Orchestration: DSPy + LangGraph + ChromaDB")
    print("="*50)

    # 1. Setup DSPy and Gemini
    print("\n[1] Initializing DSPy with Gemini API...")
    try:
        setup_dspy()
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("Please run this script with your API key:")
        print('export GEMINI_API_KEY="your_api_key_here"')
        print('uv run python main.py')
        return

    # 2. Build the LangGraph Orchestrator
    print("\n[2] Building LangGraph State Machine...")
    app = build_graph()

    # 3. Execute a Query
    test_queries = [
        "What is the main frontend framework used for Project Orion?",
        "How much funding did Project Orion raise?",
        "What kind of cake did they eat at the launch party?" # Should fail/return "I don't know"
    ]

    for query in test_queries:
        print(f"\n>>> QUERY: {query}")
        
        # Initial state
        state = {
            "question": query,
            "context": None,
            "answer": None,
            "is_correct": None,
            "retries": 0
        }
        
        # Run the graph
        for output in app.stream(state):
            # Stream yields the output of each node
            for node_name, node_state in output.items():
                pass # The nodes themselves print debug info
                
        # The final output state will be stored in the app state or can be 
        # retrieved from the last yielded output.
        # However, app.stream yields dictionaries of {node: state_updates}.
        # The final answer is best extracted directly from the node outputs:
        if "generate" in output:
            final_answer = output["generate"]["answer"]
        elif "grade" in output and "answer" in output["grade"]: # if it finished immediately
             final_answer = output["grade"]["answer"]
        else:
            final_answer = "Could not generate answer."

        print(f"FINAL ANSWER: {final_answer}")
        print("-" * 50)

if __name__ == "__main__":
    main()
