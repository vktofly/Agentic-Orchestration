import json
import urllib.request
import urllib.error
from fastapi import APIRouter

router = APIRouter()

@router.get("/models")
def get_models():
    """
    Fetches available Ollama models for auto-discovery.
    """
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            # Prefix with ollama/ so model_factory can route it
            models = [f"ollama/{m['name']}" for m in data.get("models", [])]
            return {"models": models}
    except (urllib.error.URLError, Exception) as e:
        print(f"Ollama auto-discovery failed: {e}")
        return {"models": []}
