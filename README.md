# Agentic Orchestration Framework

> A self-healing, zero-regression AI orchestrator designed for enterprise reliability.

Most AI applications rely on fragile manual prompt engineering and linear execution paths, leading to silent hallucinations and prompt rot in production. 

This framework solves those critical enterprise pain points by abandoning manual prompting in favor of **DSPy's programmatic prompt compilation**, and wrapping the agent in a **cyclical LangGraph state machine** that forces the LLM to autonomously grade and self-correct its own answers. 

Supported by a modern Next.js/FastAPI full-stack architecture and automated CI/CD quality gates, this project demonstrates how to deploy AI that doesn't break.

## Core Value Proposition

* **Self-Healing State Machine (LangGraph):** The agent never blindly outputs answers. It retrieves context, generates a draft, and passes it to an "LLM-as-a-judge" grading node. If hallucinations are detected, the agent autonomously rejects the draft and loops back to retry, ensuring high factual accuracy.
* **Promptless Orchestration (DSPy):** Eliminates brittle "prompt rot." By treating prompts like neural network weights, DSPy mathematically compiles and optimizes instructions and few-shot examples for any target LLM, guaranteeing maximum performance without manual tweaking.
* **Zero-Regression CI/CD (GitHub Actions):** Designed for DevOps integration. The framework is built to support automated G-Eval benchmarks on every pull request, enforcing strict quality gates before AI updates reach production.
* **Real-Time Observability (Next.js & FastAPI):** A decoupled full-stack architecture that streams the agent's internal reasoning states (Retrieving... Generating... Grading) directly to a modern UI, ending the "black box" AI experience.

## The State Graph Workflow
The agent runs in a continuous loop until the evaluator (Grader) determines the output is factual and hallucination-free based strictly on the retrieved context.

1. **Retrieve:** Extract relevant chunks using the vector retriever.
2. **Generate:** Use the DSPy `generate_answer` module (Chain of Thought) to synthesize a draft answer.
3. **Grade:** Evaluate the answer against the context.
   - If *PASS*, exit the graph and stream the answer to the user.
   - If *FAIL*, loop back to the Generate node (with a max retry limit) to self-correct.

## Getting Started

### 1. Install Dependencies
```bash
# Backend dependencies
uv sync

# Frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Environment Setup
Create a `.env.local` file at the root of the project with your API key:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 3. Run the Backend (FastAPI)
The backend serves the LangGraph API and handles DSPy optimization caching to reduce cold starts.
```bash
uv run uvicorn src.api.server:app --port 8000
```

### 4. Run the Frontend (Next.js)
The frontend dashboard visualizes the state graph's real-time execution.
```bash
cd frontend
npm run dev
```
