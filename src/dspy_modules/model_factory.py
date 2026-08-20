import os
import dspy

# ==============================================================================
# Factory for dynamic LLM instantiation
# ==============================================================================
def get_model(provider: str) -> dspy.LM:
    """
    Returns an instantiated DSPy Language Model based on the provider string.
    Raises ValueError if the provider is unsupported or the API key is missing.
    """
    provider = provider.lower().strip()
    
    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "your-gemini-api-key":
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        return dspy.LM('gemini/gemini-flash-latest', api_key=api_key)
        
    elif provider == "claude":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is missing.")
        # Claude 3 Haiku for speed/cost similar to Gemini Flash
        return dspy.LM('anthropic/claude-3-haiku-20240307', api_key=api_key)
        
    elif provider == "chatgpt":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is missing.")
        # GPT-4o mini for speed/cost similar to Gemini Flash
        return dspy.LM('openai/gpt-4o-mini', api_key=api_key)
        
    elif provider.startswith("ollama/"):
        model_name = provider.split("/", 1)[1]
        return dspy.LM(f'ollama_chat/{model_name}', api_base='http://localhost:11434', api_key='')
        
    else:
        raise ValueError(f"Unsupported LLM provider: '{provider}'. Supported providers are: 'gemini', 'claude', 'chatgpt', and any 'ollama/<model>'.")
