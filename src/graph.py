from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from src.vector_store import retrieve
from src.dspy_modules import RAGGenerator, RAGGrader

# Define the state of our agent across nodes
class GraphState(TypedDict):
    question: str
    context: Optional[str]
    answer: Optional[str]
    is_correct: Optional[bool]
    retries: int

def retrieve_node(state: GraphState):
    """Node: Retrieves context from ChromaDB based on the question."""
    print("---NODE: RETRIEVE---")
    question = state["question"]
    context = retrieve(question)
    return {"context": context}

def generate_node(state: GraphState):
    """Node: Uses DSPy to generate an answer based on the context."""
    print("---NODE: GENERATE---")
    generator = RAGGenerator()
    
    # If we have looped too many times, return a fallback to avoid infinite loops
    if state.get("retries", 0) > 2:
        return {"answer": "I failed to generate a correct answer after multiple attempts."}

    prediction = generator(question=state["question"], context=state["context"])
    return {"answer": prediction.answer}

def grade_node(state: GraphState):
    """Node: Uses DSPy as a judge to grade the generated answer."""
    print("---NODE: GRADE---")
    
    if state.get("retries", 0) > 2:
        return {"is_correct": True} # Force exit
        
    grader = RAGGrader()
    prediction = grader(
        question=state["question"], 
        context=state["context"], 
        answer=state["answer"]
    )
    
    is_correct_str = prediction.is_correct.strip().lower()
    is_correct = "true" in is_correct_str
    
    print(f"Grade Result: {'PASS' if is_correct else 'FAIL'} (Raw: {prediction.is_correct})")
    
    return {
        "is_correct": is_correct,
        "retries": state.get("retries", 0) + 1
    }

def decide_to_generate(state: GraphState):
    """Conditional Edge: Decide whether to finish or retry generation."""
    if state["is_correct"]:
        print("---DECISION: FINISH---")
        return END
    else:
        print("---DECISION: RETRY GENERATION---")
        return "generate"

def build_graph():
    """Compiles the LangGraph state machine."""
    workflow = StateGraph(GraphState)

    # Add Nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("grade", grade_node)

    # Set Entry Point
    workflow.set_entry_point("retrieve")

    # Define Edges
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "grade")
    workflow.add_conditional_edges(
        "grade",
        decide_to_generate,
        {
            END: END,
            "generate": "generate"
        }
    )

    # Compile the graph
    app = workflow.compile()
    return app
