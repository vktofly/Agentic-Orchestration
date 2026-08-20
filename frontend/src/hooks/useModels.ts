import { useState, useEffect } from "react";

export function useModels() {
  const [provider, setProvider] = useState("gemini");
  const [ollamaModels, setOllamaModels] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/models")
      .then((res) => res.json())
      .then((data) => {
        if (data.models && Array.isArray(data.models)) {
          setOllamaModels(data.models);
        }
      })
      .catch((err) => console.error("Failed to fetch Ollama models", err));
  }, []);

  return { provider, setProvider, ollamaModels };
}
