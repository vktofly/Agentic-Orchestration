from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    query: str  # User's question string
    provider: Optional[str] = "gemini" # LLM Provider ('gemini', 'claude', 'chatgpt')

class ChatResponse(BaseModel):
    answer: str # Verified agent output string

class EvalSetEntry(BaseModel):
    question: str
    context: Optional[List[str]] = None
    answer: str
