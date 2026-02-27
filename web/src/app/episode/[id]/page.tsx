"use client";

import { useSearchParams } from "next/navigation";

import { usePodcast } from "../../hooks/usePodcast";
import ThemeSwitcher from "../../components/ThemeSwitcher";
import AudioPlayer from "./components/AudioPlayer";
import ChatPanel from "./components/ChatPanel";
import MindMap from "./components/MindMap";
import SummaryCard from "./components/SummaryCard";

export default function EpisodePage({ params }: { params: { id: string } }) {
  const searchParams = useSearchParams();
  const summaryId = searchParams.get("summary_id") ?? undefined;
  const { status, episode, isLoading } = usePodcast(params.id, summaryId);

  const summary = episode?.summary;

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div className="flex flex-col gap-2">
            <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
              / 单集
            </div>
            <h1 className="text-3xl font-semibold">
              {episode?.title ?? "正在加载节目详情"}
            </h1>
            <p className="max-w-2xl text-sm text-[var(--ink-muted)]">
              {episode?.description ?? "处理完成后将显示摘要与问答。"}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <ThemeSwitcher />
          </div>
        </div>

        {status?.status && (
          <div className="mt-6 inline-flex items-center rounded-full border border-[var(--border)] bg-[var(--panel-translucent)] px-4 py-2 text-xs font-semibold text-[var(--ink-muted)]">
            状态：{status.status}
          </div>
        )}

        <div className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-6">
            <AudioPlayer audioUrl={episode?.audio_url} title={episode?.title} />
            <SummaryCard
              summaryText={summary?.summary_text}
              oneSentence={summary?.one_sentence_summary}
              keyTakeaways={summary?.key_takeaways}
            />
            <MindMap data={summary?.mind_map_structure} />
          </div>
          <div className="space-y-6">
            <ChatPanel episodeId={Number(params.id)} />
            {isLoading && (
              <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6 text-sm text-[var(--ink-muted)]">
                加载中，请稍候。
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
