"use client";

import { useTranslations } from "next-intl";

type SummaryCardProps = {
  summaryText?: string | null;
  oneSentence?: string | null;
  keyTakeaways?: string[] | null;
};

export default function SummaryCard({
  summaryText,
  oneSentence,
  keyTakeaways,
}: SummaryCardProps) {
  const t = useTranslations("Summary");

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
        {t("kicker")}
      </div>
      <h2 className="mt-3 text-xl font-semibold">
        {oneSentence ?? t("loadingTitle")}
      </h2>
      {summaryText && <p className="mt-4 text-sm text-[var(--ink-muted)]">{summaryText}</p>}
      {keyTakeaways && keyTakeaways.length > 0 && (
        <div className="mt-6">
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
            {t("keyTakeaways")}
          </div>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-[var(--ink-muted)]">
            {keyTakeaways.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
