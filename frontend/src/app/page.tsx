"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Bot, Loader2 } from "lucide-react";
import DiffViewer from "@/components/DiffViewer";
import ScrubBar from "@/components/ScrubBar";

import { useModels } from "@/hooks/useModels";
import { useAgentStream } from "@/hooks/useAgentStream";

import ProviderSelect from "@/components/ProviderSelect";
import ChatBubble from "@/components/ChatBubble";
import MessageInput from "@/components/MessageInput";

export default function Home() {
  const { provider, setProvider, ollamaModels } = useModels();
  const { messages, isLoading, handleSubmit, handleEvalSubmit } = useAgentStream(provider);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8 text-center"
      >
        <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2 flex items-center justify-center gap-3">
          <Sparkles className="w-8 h-8 text-blue-400" />
          Agentic Orchestration
        </h1>
        <p className="text-slate-300">DSPy + LangGraph Autonomous Pipeline</p>
      </motion.div>

      {/* Chat Container (Glassmorphism) */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-3xl bg-slate-900/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl overflow-hidden flex flex-col h-[70vh]"
      >
        <ProviderSelect provider={provider} setProvider={setProvider} ollamaModels={ollamaModels} />

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <AnimatePresence>
            {messages.map((msg) => (
              <ChatBubble key={msg.id} msg={msg} isLoading={isLoading} onEval={handleEvalSubmit} />
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-4 flex-row"
            >
              <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 text-emerald-400" />
              </div>
              <div className="px-5 py-3 rounded-2xl bg-slate-800/50 border border-slate-700 flex items-center gap-3">
                <Loader2 className="w-5 h-5 text-emerald-400 animate-spin" />
                <span className="text-slate-400 text-sm">
                  Orchestrating agents ({provider})...
                </span>
              </div>
            </motion.div>
          )}
        </div>

        <MessageInput isLoading={isLoading} provider={provider} onSubmit={handleSubmit} />
      </motion.div>

      {/* Advanced UI Sections */}
      <div className="w-full max-w-3xl mt-8 flex flex-col gap-8">
        <DiffViewer />
        {messages
          .map((m) => m.thread_id && <ScrubBar key={m.thread_id} threadId={m.thread_id} />)
          .pop()}
      </div>
    </main>
  );
}
