import { motion } from "framer-motion";
import { Bot, User, Activity, ThumbsUp, ThumbsDown } from "lucide-react";
import { Message } from "@/types/chat";

interface ChatBubbleProps {
  msg: Message;
  isLoading: boolean;
  onEval: (msg: Message, type: "golden" | "negative") => void;
}

export default function ChatBubble({ msg, isLoading, onEval }: ChatBubbleProps) {
  const isUser = msg.role === "user";
  const hasErrors = msg.traces?.some((t) => t.is_valid === false || (t.retries && t.retries > 0));

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-4 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
          isUser ? "bg-blue-500" : "bg-slate-700"
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-emerald-400" />
        )}
      </div>

      <div
        className={`px-5 py-3 rounded-2xl max-w-[80%] transition-colors duration-500 ${
          isUser
            ? "bg-blue-500/20 text-blue-50 border border-blue-500/30"
            : hasErrors
            ? "bg-rose-900/20 text-slate-200 border border-rose-500/50 shadow-[0_0_15px_rgba(225,29,72,0.15)]"
            : "bg-slate-800/50 text-slate-200 border border-slate-700"
        }`}
      >
        {msg.traces && msg.traces.length > 0 && (
          <div className="mb-3 flex flex-wrap gap-2">
            {msg.traces.map((trace, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 px-2 py-1 bg-slate-900/80 rounded border border-slate-600 text-xs text-slate-300"
              >
                <Activity className="w-3 h-3 text-emerald-500" />
                {trace.name}
                {trace.is_valid !== undefined && (
                  <span className={trace.is_valid ? "text-emerald-400" : "text-rose-400"}>
                    {trace.is_valid ? "(valid)" : "(invalid)"}
                  </span>
                )}
                {trace.retries !== undefined && trace.retries > 0 && (
                  <span className="text-amber-400">(retry: {trace.retries})</span>
                )}
              </span>
            ))}
          </div>
        )}
        {msg.content ? (
          <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
        ) : msg.role === "assistant" ? (
          <div className="flex gap-1 items-center h-6">
            <span className="w-2 h-2 rounded-full bg-slate-500 animate-pulse"></span>
            <span className="w-2 h-2 rounded-full bg-slate-500 animate-pulse delay-75"></span>
            <span className="w-2 h-2 rounded-full bg-slate-500 animate-pulse delay-150"></span>
          </div>
        ) : null}

        {msg.role === "assistant" && msg.content && !isLoading && (
          <div className="mt-4 pt-3 border-t border-slate-700/50 flex items-center justify-end gap-2">
            <span className="text-xs text-slate-500 mr-2">Capture Eval:</span>
            <button
              onClick={() => onEval(msg, "golden")}
              className="p-1.5 hover:bg-emerald-500/20 hover:text-emerald-400 text-slate-400 rounded transition-colors"
              title="Add to Golden Eval Set"
            >
              <ThumbsUp className="w-4 h-4" />
            </button>
            <button
              onClick={() => onEval(msg, "negative")}
              className="p-1.5 hover:bg-rose-500/20 hover:text-rose-400 text-slate-400 rounded transition-colors"
              title="Add to Negative Eval Set"
            >
              <ThumbsDown className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
}
