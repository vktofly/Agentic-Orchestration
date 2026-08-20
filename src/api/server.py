import numpy # Fix circular import with DSPy lazy loader
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.ai_pipeline import init_ai_pipeline, close_ai_pipeline, get_graph_app
from src.api.routers import chat, models, evals

# ==============================================================================
# FastAPI Application Lifecycle
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_ai_pipeline()
    yield
    # Shutdown
    await close_ai_pipeline()

# ==============================================================================
# FastAPI Application Configuration
# ==============================================================================
app = FastAPI(
    title="Agentic Orchestration API",
    description="API for DSPy + LangGraph agent",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# API Routers
# ==============================================================================
app.include_router(chat.router, prefix="/api", tags=["Chat & Orchestration"])
app.include_router(models.router, prefix="/api", tags=["Models"])
app.include_router(evals.router, prefix="/api", tags=["Evaluations"])

# ==============================================================================
# Core Endpoints
# ==============================================================================
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify backend status and AI readiness.
    """
    graph_app = get_graph_app()
    return {"status": "ok", "ai_ready": graph_app is not None}
