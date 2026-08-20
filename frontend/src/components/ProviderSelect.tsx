import { Settings2 } from "lucide-react";

interface ProviderSelectProps {
  provider: string;
  setProvider: (provider: string) => void;
  ollamaModels: string[];
}

export default function ProviderSelect({ provider, setProvider, ollamaModels }: ProviderSelectProps) {
  return (
    <div className="px-6 py-3 border-b border-slate-700/50 bg-slate-900/60 flex justify-between items-center">
      <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
        Multi-Agent Sandbox
      </span>
      <div className="flex items-center gap-2">
        <Settings2 className="w-4 h-4 text-slate-400" />
        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value)}
          className="bg-slate-800 border border-slate-600 text-slate-200 text-sm rounded-lg px-2 py-1 focus:ring-blue-500 focus:border-blue-500 outline-none"
          title="Select LLM Provider"
        >
          <option value="gemini">Google Gemini</option>
          <option value="claude">Anthropic Claude</option>
          <option value="chatgpt">OpenAI ChatGPT</option>
          {ollamaModels.length > 0 && (
            <optgroup label="Local Ollama Models">
              {ollamaModels.map((model) => (
                <option key={model} value={model}>
                  {model.replace("ollama/", "")}
                </option>
              ))}
            </optgroup>
          )}
        </select>
      </div>
    </div>
  );
}
