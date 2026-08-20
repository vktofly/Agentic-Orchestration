# Agentic Orchestration

> A self-healing, zero-regression AI orchestrator designed for enterprise reliability.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

Most AI applications rely on fragile manual prompt engineering and linear execution paths, leading to silent hallucinations and prompt rot in production. 

This framework solves those critical enterprise pain points by abandoning manual prompting in favor of **DSPy's programmatic prompt compilation**, and wrapping the agent in a **cyclical LangGraph state machine** that forces the LLM to autonomously grade and self-correct its own answers. 

Supported by a modern Next.js/FastAPI full-stack architecture, this project demonstrates how to deploy AI that doesn't break.

## Core Value Proposition

* **Self-Healing State Machine (LangGraph):** The agent never blindly outputs answers. It retrieves context, generates a draft, and passes it to an "LLM-as-a-judge" grading node. If hallucinations are detected, the agent autonomously rejects the draft and loops back to retry, ensuring high factual accuracy.
* **Promptless Orchestration (DSPy):** Eliminates brittle "prompt rot." By treating prompts like neural network weights, DSPy mathematically compiles and optimizes instructions for any target LLM.
* **Dependency Inversion Vector Store:** Built with enterprise patterns in mind, the retriever is an abstract interface that easily swaps between in-memory `Dummy` stores for rapid local testing and real `ChromaDB` instances for production.
* **Real-Time Observability (Next.js & FastAPI):** A decoupled full-stack architecture that streams the agent's internal reasoning states (Retrieving... Generating... Grading) directly to a modern UI.

## Getting Started

### 1. Environment Setup
Create a `.env.local` file at the root of the project with your API key:
```env
GEMINI_API_KEY="your_api_key_here"

# Set to "dummy" to bypass C++ dependencies locally, or "chromadb" for production
VECTOR_STORE_TYPE=dummy
```

### 2. Run with Docker (Recommended)
This repository includes a `docker-compose.yml` configured for zero-setup deployments.

```bash
docker compose up --build
```
* **Frontend:** `http://localhost:3000`
* **Backend API:** `http://localhost:8000`

### 3. Run Locally (Without Docker)

#### Install Dependencies
```bash
# Backend dependencies (using uv)
uv sync

# Frontend dependencies
cd frontend
npm install
cd ..
```

#### Run the Backend
```bash
uv run uvicorn src.api.server:app --port 8000
```

#### Run the Frontend
In a new terminal:
```bash
cd frontend
npm run dev
```
Navigate to `http://localhost:3000`.

## Architecture Details

- **Backend (`src/`)**: Python FastAPI using `uv` for ultra-fast dependency resolution.
- **Agent Orchestrator (`src/graph/agent.py`)**: Defines the LangGraph execution flow. 
- **Checkpointer (`aiosqlite`)**: Handles concurrent LLM state histories for production threadpools.
- **Frontend (`frontend/`)**: React 19 / Next.js 15 streaming interface using Server-Sent Events (SSE).

## License

MIT License
