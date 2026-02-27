"use client";

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
  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
        / 摘要
      </div>
      <h2 className="mt-3 text-xl font-semibold">
        {oneSentence ?? "正在生成摘要..."}
      </h2>
      {summaryText && <p className="mt-4 text-sm text-[var(--ink-muted)]">{summaryText}</p>}
      {keyTakeaways && keyTakeaways.length > 0 && (
        <div className="mt-6">
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
            要点
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
