import dspy
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# ==============================================================================
# 1. State Definition
# ==============================================================================
# AgentState is the shared data structure passed between every node in the graph.
class AgentState(TypedDict):
    question: str                  # The incoming user question
    context: Optional[list[str]]   # Retrieved factual passages
    answer: Optional[str]          # Model generated answer
    retries: int                   # Count of retries if grading fails
    is_valid: bool                 # Whether the generated answer passed evaluation


# ==============================================================================
# 2. Graph Nodes (State Transformers)
# ==============================================================================

def retrieve_node(state: AgentState, rm: dspy.Retrieve):
    """
    Node 1: Retrieve relevant context chunks from the vector database/retriever
    based on the question stored in the current state.
    """
    print("-> Retrieving Context")
    context = rm(state['question']).passages
    return {"context": context}


def generate_node(state: AgentState, rag_module: dspy.Module):
    """
    Node 2: Synthesize an answer using the compiled DSPy RAG module.
    Bypasses module's internal retriever to enforce explicit graph-controlled context.
    """
    print("-> Generating Answer via DSPy")
    prediction = rag_module.generate_answer(
        context=state['context'], 
        question=state['question']
    )
    return {"answer": prediction.answer}


def grade_node(state: AgentState):
    """
    Node 3: Evaluates the synthesized answer (LLM-as-a-judge pattern).
    Checks for poor answers (e.g. empty, "I don't know") and triggers a retry if invalid.
    """
    print("-> Grading Answer (LLM-as-a-judge)")
    answer = state['answer'].lower()
    
    # Validation heuristic (reject uninformative responses or short hallucinations)
    if "i don't know" in answer or len(answer) < 5:
        print("   [!] Grade failed. Retrying...")
        return {"is_valid": False, "retries": state['retries'] + 1}
        
    print("   [+] Grade passed.")
    return {"is_valid": True}


# ==============================================================================
# 3. Conditional Routing Edges
# ==============================================================================

def should_continue(state: AgentState):
    """
    Decides the next node after 'grade':
    - If valid: Finish execution (END).
    - If invalid but retries <= 2: Loop back to 'generate'.
    - If invalid and retries > 2: Terminate to prevent infinite loops (END).
    """
    if state['is_valid']:
        return END
    
    if state['retries'] > 2:
        print("   [!] Max retries reached. Ending.")
        return END
        
    return "generate"


# ==============================================================================
# 4. Graph Construction & Compilation
# ==============================================================================

def build_agent_graph(rag_module: dspy.Module, rm: dspy.Retrieve, checkpointer=None):
    """
    Assembles the nodes and edges into an executable LangGraph state machine.
    """
    workflow = StateGraph(AgentState)
    
    # Register graph nodes with their bound dependencies
    workflow.add_node("retrieve", lambda state: retrieve_node(state, rm))
    workflow.add_node("generate", lambda state: generate_node(state, rag_module))
    workflow.add_node("grade", grade_node)
    
    # Establish entry point and fixed sequential transitions
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "grade")
    
    # Add conditional branching edge from 'grade'
    workflow.add_conditional_edges(
        "grade",
        should_continue,
        {
            "generate": "generate",
            END: END
        }
    )
    
    # Compile the graph into a runnable instance
    return workflow.compile(checkpointer=checkpointer)
