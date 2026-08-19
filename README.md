# Agentic Orchestration (DSPy + LangGraph)

An MLOps architecture demonstrating advanced Agentic orchestration, abandoning manual "prompt engineering" in favor of programmatic prompt compilation using **DSPy**, and wrapping the agent in a cyclic state machine using **LangGraph**.

## Architecture
- **Orchestration:** `langgraph` (Creates a cyclical State Graph)
- **Prompt Optimization & Generation:** `dspy-ai` (Using the Gemini API)
- **Vector Database:** `chromadb` (Local persistence)

## The State Graph
The agent runs in a continuous loop until the evaluator (Grader) determines the output is factual and hallucinaton-free based strictly on the retrieved context.
1. **Retrieve:** Extract relevant chunks from ChromaDB.
2. **Generate:** Use the DSPy `RAGGenerator` (Chain of Thought) to synthesize an answer.
3. **Grade:** Use the DSPy `RAGGrader` (Predict) to evaluate the answer against the context.
   - If *PASS*, exit the graph and return the answer to the user.
   - If *FAIL*, loop back to the Generate node to try again (with a max retry limit).

## How to Run

1. **Install dependencies:**
```bash
uv sync
```

2. **Set your Gemini API Key:**
Because DSPy requires a real LLM to compile and evaluate prompts, you must supply your Gemini API Key.
```bash
# Windows (Git Bash) / Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

3. **Execute the Agent:**
```bash
uv run python main.py
```
