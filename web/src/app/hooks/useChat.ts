import { useState } from "react";

import { authorizedFetch } from "../lib/api-client";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

type ChatSource = {
  text?: string;
  time: number;
  similarity?: number;
};

export function useChat(episodeId: number) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sources, setSources] = useState<ChatSource[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (content: string) => {
    setIsLoading(true);
    setMessages((prev) => [...prev, { role: "user", content }]);
    try {
      const response = await authorizedFetch<{
        answer: string;
        sources: ChatSource[];
      }>("/api/podcast/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ episode_id: episodeId, query: content }),
      });
      setMessages((prev) => [...prev, { role: "assistant", content: response.answer }]);
      setSources(response.sources || []);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Request failed.";
      setMessages((prev) => [...prev, { role: "assistant", content: message }]);
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, sources, sendMessage, isLoading };
}
