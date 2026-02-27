"use client";

import { FormEvent, useState } from "react";
import { useTranslations } from "next-intl";

import { useChat } from "../../../../hooks/useChat";
import { usePlayerStore } from "../../../../store/player";

type ChatPanelProps = {
  episodeId: number;
};

export default function ChatPanel({ episodeId }: ChatPanelProps) {
  const { messages, sources, sendMessage, isLoading } = useChat(episodeId);
  const [input, setInput] = useState("");
  const seekTo = usePlayerStore((state) => state.seekTo);
  const t = useTranslations("ChatPanel");

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
        {t("kicker")}
      </div>
      <div className="mt-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`rounded-2xl px-4 py-3 text-sm ${
              message.role === "user"
                ? "bg-[var(--accent)] text-white"
                : "bg-[var(--bg-muted)] text-[var(--ink)]"
            }`}
          >
            {message.content}
          </div>
        ))}
        {messages.length === 0 && (
          <p className="text-sm text-[var(--ink-muted)]">{t("emptyState")}</p>
        )}
      </div>
      <form onSubmit={onSubmit} className="mt-5 flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder={t("placeholder")}
          className="flex-1 rounded-full border border-[var(--border)] px-4 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-full bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
        >
          {isLoading ? t("thinking") : t("send")}
        </button>
      </form>
      {sources.length > 0 && (
        <div className="mt-6">
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
            {t("sources")}
          </div>
          <div className="mt-3 space-y-2">
            {sources.map((source, index) => (
              <button
                key={`${source.time}-${index}`}
                onClick={() => seekTo(source.time)}
                className="w-full rounded-xl border border-[var(--border)] bg-[var(--panel)] px-3 py-2 text-left text-xs text-[var(--ink-muted)] hover:text-[var(--ink)]"
              >
                <div className="font-semibold text-[var(--ink)]">{Math.floor(source.time)}s</div>
                <div className="mt-1">{source.text}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
