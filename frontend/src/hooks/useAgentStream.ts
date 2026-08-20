import { useState } from "react";
import { Message, TraceEvent } from "@/types/chat";

export function useAgentStream(provider: string) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I am the Agentic Orchestrator. How can I help you today?",
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (input: string) => {
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg.content, provider }),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch response from API");
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No reader available");
      const decoder = new TextDecoder("utf-8");

      const aiMsgId = (Date.now() + 1).toString();
      setMessages((prev) => [...prev, { id: aiMsgId, role: "assistant", content: "", traces: [] }]);

      let aiContent = "";
      let aiTraces: TraceEvent[] = [];

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.replace("data: ", "").trim();
            if (!dataStr) continue;

            try {
              const data = JSON.parse(dataStr);
              if (data.type === "thread") {
                setMessages((prev) =>
                  prev.map((m) => (m.id === aiMsgId ? { ...m, thread_id: data.thread_id } : m))
                );
              } else if (data.type === "node") {
                aiTraces = [
                  ...aiTraces,
                  {
                    name: data.name,
                    is_valid: data.state_updates?.is_valid,
                    retries: data.state_updates?.retries,
                  },
                ];
                setMessages((prev) =>
                  prev.map((m) => (m.id === aiMsgId ? { ...m, traces: aiTraces } : m))
                );
              } else if (data.type === "answer") {
                aiContent = data.content;
                setMessages((prev) =>
                  prev.map((m) => (m.id === aiMsgId ? { ...m, content: aiContent } : m))
                );
              } else if (data.type === "error") {
                aiContent = "Error: " + data.content;
                setMessages((prev) =>
                  prev.map((m) => (m.id === aiMsgId ? { ...m, content: aiContent } : m))
                );
              }
            } catch (e) {
              console.error("Error parsing JSON", e);
            }
          }
        }
      }
    } catch (error: any) {
      console.error(error);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Error: ${error.message || "Could not reach the AI backend."}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEvalSubmit = async (msg: Message, type: "golden" | "negative") => {
    const msgIndex = messages.findIndex((m) => m.id === msg.id);
    const userMsg = messages
      .slice(0, msgIndex)
      .reverse()
      .find((m) => m.role === "user");

    if (!userMsg) return;

    const payload: any = {
      question: userMsg.content,
      answer: msg.content,
      context: [],
    };

    if (msg.thread_id) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/history/${msg.thread_id}`);
        const data = await res.json();
        const lastState = data.history[data.history.length - 1];
        if (lastState && lastState.values.context) {
          payload.context = lastState.values.context;
        }
      } catch (err) {
        console.error("Could not fetch context for eval", err);
      }
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/evalset/${type}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        alert(`Saved to ${type} eval set!`);
      }
    } catch (e) {
      console.error(e);
      alert("Failed to save eval.");
    }
  };

  return { messages, isLoading, handleSubmit, handleEvalSubmit };
}
