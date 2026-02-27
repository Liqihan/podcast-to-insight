"use client";

import { useEffect, useRef } from "react";

import { usePlayerStore } from "../../../store/player";

type AudioPlayerProps = {
  audioUrl?: string | null;
  title?: string | null;
};

export default function AudioPlayer({ audioUrl, title }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const { targetTime, clearTarget, setCurrentTime } = usePlayerStore((state) => state);

  useEffect(() => {
    if (!audioRef.current || targetTime === null) return;
    audioRef.current.currentTime = targetTime;
    audioRef.current.play().catch(() => undefined);
    clearTarget();
  }, [targetTime, clearTarget]);

  if (!audioUrl) {
    return (
      <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
        <p className="text-sm text-[var(--ink-muted)]">音频尚未就绪。</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
      <div className="text-sm font-semibold">{title ?? "音频"}</div>
      <audio
        ref={audioRef}
        className="mt-3 w-full"
        controls
        src={audioUrl}
        onTimeUpdate={(event) => setCurrentTime(event.currentTarget.currentTime)}
      />
    </div>
  );
}
