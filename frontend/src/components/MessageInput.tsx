import { useState } from "react";
import { Send } from "lucide-react";

interface MessageInputProps {
  isLoading: boolean;
  provider: string;
  onSubmit: (input: string) => void;
}

export default function MessageInput({ isLoading, provider, onSubmit }: MessageInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSubmit(input);
    setInput("");
  };

  return (
    <div className="p-4 bg-slate-900/60 border-t border-slate-700/50">
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Ask the agent a question (using ${provider})...`}
          className="w-full bg-slate-800/50 border border-slate-600 rounded-xl py-4 pl-5 pr-14 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="absolute right-2 p-2 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 disabled:hover:bg-blue-500 rounded-lg transition-colors"
        >
          <Send className="w-5 h-5 text-white" />
        </button>
      </form>
    </div>
  );
}
