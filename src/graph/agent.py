import uuid
from typing import AsyncGenerator
import dspy

from src.api.ai_pipeline import get_graph_app
from src.dspy_modules.model_factory import get_model

async def stream_agent_execution(query: str, provider: str) -> AsyncGenerator[dict, None]:
    """
    Deep Module for Agent Execution.
    Encapsulates DSPy context management, LangGraph state initialization, and iteration.
    Yields parsed state dictionary events instead of raw LangGraph structures.
    """
    graph_app = get_graph_app()
    if not graph_app:
        yield {"type": "error", "content": "AI pipeline not initialized."}
        return
        
    try:
        model = get_model(provider)
    except ValueError as e:
        yield {"type": "error", "content": str(e)}
        return
        
    state = {
        "question": query,
        "context": None,
        "answer": None,
        "is_valid": False,
        "retries": 0
    }
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    yield {"type": "thread", "thread_id": thread_id}
    
    try:
        iterator = graph_app.astream(state, config=config)
        final_answer = "Could not generate answer."
        
        while True:
            # Enter context only for the graph execution step
            with dspy.context(lm=model):
                try:
                    output = await iterator.__anext__()
                except StopAsyncIteration:
                    break
                    
            node_name = list(output.keys())[0]
            node_state = output[node_name]
            
            event_data = {
                "type": "node",
                "name": node_name,
                "state_updates": {}
            }
            
            if "is_valid" in node_state:
                event_data["state_updates"]["is_valid"] = node_state["is_valid"]
            if "retries" in node_state:
                event_data["state_updates"]["retries"] = node_state["retries"]
                
            yield event_data
            
            if node_name in ["generate", "grade"] and "answer" in node_state:
                final_answer = node_state["answer"]
                
        yield {"type": "answer", "content": final_answer}
    except Exception as e:
        yield {"type": "error", "content": str(e)}


async def get_agent_history(thread_id: str) -> list:
    """
    Deep Module for fetching agent history.
    Abstracts away the LangGraph Checkpointer interface.
    """
    graph_app = get_graph_app()
    if not graph_app:
        raise ValueError("AI pipeline not initialized.")
        
    config = {"configurable": {"thread_id": thread_id}}
    history = []
    async for s in graph_app.aget_state_history(config):
        history.append({
            "values": s.values,
            "next": list(s.next) if s.next else []
        })
    history.reverse()
    return history
