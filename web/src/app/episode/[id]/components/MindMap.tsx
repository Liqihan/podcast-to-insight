type MindMapProps = {
  data?: Record<string, unknown> | null;
};

function renderNode(node: Record<string, any>, level = 0) {
  const entries = Object.entries(node);
  return (
    <div className="space-y-2">
      {entries.map(([key, value]) => (
        <div key={`${level}-${key}`} className="rounded-xl border border-[var(--border)] bg-white/70 p-3">
          <div className="text-sm font-semibold">{key}</div>
          {value && typeof value === "object" && (
            <div className="mt-2 pl-2">{renderNode(value as Record<string, any>, level + 1)}</div>
          )}
          {value && typeof value !== "object" && (
            <div className="mt-2 text-sm text-[var(--ink-muted)]">{String(value)}</div>
          )}
        </div>
      ))}
    </div>
  );
}

export default function MindMap({ data }: MindMapProps) {
  return (
    <div className="rounded-2xl border border-[var(--border)] bg-white p-6">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
        / Mind map
      </div>
      <div className="mt-4 text-sm text-[var(--ink-muted)]">
        {data ? renderNode(data) : "Mind map is not available yet."}
      </div>
    </div>
  );
}
