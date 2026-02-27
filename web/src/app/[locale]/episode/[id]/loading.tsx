"use client";

import { useTranslations } from "next-intl";

export default function LoadingEpisode() {
  const t = useTranslations("Loading");

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="rounded-3xl border border-[var(--border)] bg-[var(--panel)] p-10">
          <div className="text-sm text-[var(--ink-muted)]">{t("loading")}</div>
        </div>
      </div>
    </div>
  );
}
