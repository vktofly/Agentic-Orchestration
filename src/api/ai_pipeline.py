import os
from pathlib import Path
from dotenv import load_dotenv
import dspy
import aiosqlite

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from src.vector_store.factory import get_retriever
from src.dspy_modules.qa_system import compile_rag_module
from src.graph.orchestrator import build_agent_graph

# Global state for the application
graph_app = None
db_conn = None

async def init_ai_pipeline():
    """
    Initializes the AI pipeline: DSPy global settings, LangGraph agent, and DB connections.
    """
    global graph_app, db_conn
    
    try:
        env_path = Path.cwd() / ".env.local"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        
        # Configure global DSPy Retrieval Model
        rm = get_retriever()
        dspy.settings.configure(rm=rm)
        
        # Initialize Async SQLite Checkpointer
        db_conn = await aiosqlite.connect("checkpoints.sqlite")
        memory = AsyncSqliteSaver(db_conn)
        
        # Load optimized DSPy module and assemble LangGraph agent
        compiled_rag = compile_rag_module(auto_compile=False)
        retriever = dspy.Retrieve(k=2)
        graph_app = build_agent_graph(compiled_rag, retriever, checkpointer=memory)
        print("AI Pipeline initialized successfully (Async).")
    except Exception as e:
        print(f"Warning: Failed to initialize AI components: {e}")
        graph_app = None

def get_graph_app():
    return graph_app

async def close_ai_pipeline():
    global db_conn
    if db_conn:
        await db_conn.close()
