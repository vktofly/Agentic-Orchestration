import json
from pathlib import Path
from fastapi import APIRouter
from src.api.schemas import EvalSetEntry

router = APIRouter()

@router.get("/prompt-diff")
def prompt_diff():
    """
    Returns the base signature and the optimized prompt from DSPy cache.
    """
    cache_path = Path.cwd() / "src" / "dspy_modules" / "compiled_rag.json"
    
    base_prompt = {
        "instruction": "Answer questions with short, precise, factual answers based on the context.",
        "fields": ["context", "question", "answer"],
        "demos": []
    }
    
    optimized_prompt = None
    if cache_path.exists():
        try:
            with open(cache_path, "r") as f:
                data = json.load(f)
                optimized_prompt = {
                    "instruction": data.get("signature_instructions", base_prompt["instruction"]),
                    "fields": base_prompt["fields"],
                    "demos": data.get("demos", [])
                }
        except Exception as e:
            print(f"Failed to read prompt cache: {e}")
            
    return {
        "base": base_prompt,
        "optimized": optimized_prompt
    }

@router.post("/evalset/golden")
def add_golden_eval(entry: EvalSetEntry):
    """
    Appends a successful run to the golden evaluation set.
    """
    eval_file = Path.cwd() / "eval_golden.jsonl"
    try:
        with open(eval_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.model_dump()) + "\n")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/evalset/negative")
def add_negative_eval(entry: EvalSetEntry):
    """
    Appends a failed run to the negative evaluation set.
    """
    eval_file = Path.cwd() / "eval_negative.jsonl"
    try:
        with open(eval_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.model_dump()) + "\n")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
