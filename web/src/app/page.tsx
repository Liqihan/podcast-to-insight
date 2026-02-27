const features = [
  {
    title: "Instant episode intelligence",
    description:
      "Paste a podcast link and get structured highlights, decisions, and key quotes in seconds.",
  },
  {
    title: "Reliable summaries at scale",
    description:
      "Chunking, deduplication, and multi-pass synthesis keep long-form audio accurate and consistent.",
  },
  {
    title: "Built for teams and workflows",
    description:
      "Export insights to docs, share transcripts, and keep the source audio traceable.",
  },
];

const stats = [
  { value: "58k+", label: "Episodes processed" },
  { value: "3.2x", label: "Faster research cycles" },
  { value: "92%", label: "Insight reuse rate" },
  { value: "24/7", label: "Always-on analysis" },
];

const benchmarks = [
  "Podcast QA",
  "Topic recall",
  "Speaker attribution",
  "Long-form summaries",
];

const press = [
  {
    title: "Audio to action in minutes",
    outlet: "Product Review",
    quote:
      "The closest thing to a research assistant for podcasts. Fast, clean, and remarkably consistent.",
  },
  {
    title: "A calm interface for deep work",
    outlet: "Design Week",
    quote:
      "The UI stays out of the way while the insight layer does the heavy lifting.",
  },
  {
    title: "A new default for teams",
    outlet: "SaaS Today",
    quote:
      "Podcasts become searchable, citeable, and shareable—without manual transcription.",
  },
];

const logos = [
  "Northwind",
  "Layer9",
  "Kiteworks",
  "Studio 11",
  "Everglow",
  "Signal Labs",
];

export default function Home() {
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mt-6 flex items-center justify-center rounded-full border border-[var(--border)] bg-white/70 px-4 py-2 text-xs font-medium text-[var(--ink-muted)] backdrop-blur">
          Big news: Podcast Insight is now in private beta.{" "}
          <span className="ml-1 text-[var(--ink)]">Request access →</span>
        </div>

        <header className="mt-6 flex items-center justify-between">
          <div className="flex items-center gap-2 text-base font-semibold">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--ink)] text-white">
              P
            </span>
            PodInsight
          </div>
          <nav className="hidden items-center gap-8 text-sm font-medium text-[var(--ink-muted)] md:flex">
            <span className="text-[var(--ink)]">Product</span>
            <span>Pricing</span>
            <span>Docs</span>
            <span>Blog</span>
          </nav>
          <div className="flex items-center gap-3 text-sm">
            <button className="hidden rounded-full border border-[var(--border)] px-4 py-2 text-[var(--ink)] md:inline-flex">
              Log in
            </button>
            <button className="rounded-full bg-[var(--ink)] px-4 py-2 text-white">
              Try it out
            </button>
          </div>
        </header>

        <section className="relative mt-16 overflow-hidden rounded-3xl border border-[var(--border)] bg-white/80 p-10 shadow-[0_40px_120px_rgba(20,20,20,0.08)] backdrop-blur">
          <div className="absolute right-[-120px] top-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(255,216,173,0.75),rgba(255,216,173,0))]" />
          <div className="absolute left-[-120px] bottom-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(173,210,255,0.7),rgba(173,210,255,0))]" />
          <div className="relative">
            <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
              / podcast insight layer
            </div>
            <h1 className="mt-6 max-w-2xl text-4xl font-semibold tracking-tight md:text-5xl font-display">
              Turn podcasts into actionable intelligence.
            </h1>
            <p className="mt-4 max-w-2xl text-lg text-[var(--ink-muted)]">
              Connect audio to your workflows. Extract themes, decisions, and
              citations that teams can trust.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <button className="rounded-full bg-[var(--ink)] px-6 py-3 text-sm font-semibold text-white">
                Try a demo
              </button>
              <button className="rounded-full border border-[var(--border)] bg-white px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                Talk to an expert
              </button>
            </div>

            <div className="mt-10 rounded-2xl border border-[var(--border)] bg-white p-4 shadow-sm">
              <div className="flex flex-col gap-3 md:flex-row md:items-center">
                <div className="flex h-11 flex-1 items-center rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-4 text-sm text-[var(--ink-muted)]">
                  Paste a podcast link or upload audio
                </div>
                <div className="flex flex-wrap gap-2">
                  {["summarize", "outline", "extract", "research"].map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-[var(--border)] bg-white px-3 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-[var(--ink-muted)]"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-[var(--ink-muted)]">
                <span>Example: "What did the guest say about RLHF safety?"</span>
                <span className="h-1 w-1 rounded-full bg-[var(--ink-muted)]" />
                <span>Instant citations and timestamps</span>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-10 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm font-medium text-[var(--ink-muted)]">
            Trusted by researchers, founders, and media teams
          </p>
          <div className="flex flex-wrap gap-6 text-sm font-semibold text-[var(--ink-muted)]">
            {logos.map((logo) => (
              <span key={logo}>{logo}</span>
            ))}
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / the workflow layer
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            Loved by researchers. Built for teams.
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">
            Everything you need to go from audio to decision-ready summaries,
            without manual transcription or messy docs.
          </p>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-sm"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--bg-muted)] text-sm font-semibold">
                  {index + 1}
                </div>
                <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
                <p className="mt-2 text-sm text-[var(--ink-muted)]">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24 rounded-3xl border border-[var(--border)] bg-white p-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / benchmarks
          </div>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
            <h2 className="text-3xl font-semibold tracking-tight md:text-4xl font-display">
              Audio search grounded in evidence.
            </h2>
            <button className="rounded-full border border-[var(--border)] bg-white px-4 py-2 text-sm font-semibold text-[var(--ink)]">
              View methodology
            </button>
          </div>
          <div className="mt-6 flex flex-wrap gap-3">
            {benchmarks.map((label, index) => (
              <span
                key={label}
                className={`rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.14em] ${
                  index === 0
                    ? "bg-[var(--ink)] text-white"
                    : "border border-[var(--border)] text-[var(--ink-muted)]"
                }`}
              >
                {label}
              </span>
            ))}
          </div>

          <div className="mt-8 grid gap-6 md:grid-cols-[1.2fr_1fr]">
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--bg-muted)] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                Podcast QA score
              </p>
              <div className="mt-4 text-5xl font-semibold">92.4</div>
              <p className="mt-2 text-sm text-[var(--ink-muted)]">
                Consistent summaries across 60+ hours of long-form audio.
              </p>
            </div>
            <div className="rounded-2xl border border-[var(--border)] bg-white p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                Evidence coverage
              </p>
              <div className="mt-4 space-y-3 text-sm text-[var(--ink-muted)]">
                <div className="flex items-center justify-between">
                  <span>Speaker attribution</span>
                  <span className="font-semibold text-[var(--ink)]">94%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Citation density</span>
                  <span className="font-semibold text-[var(--ink)]">87%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Topic coverage</span>
                  <span className="font-semibold text-[var(--ink)]">91%</span>
                </div>
              </div>
              <button className="mt-6 w-full rounded-full bg-[var(--ink)] py-3 text-sm font-semibold text-white">
                Run your own benchmark
              </button>
            </div>
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / proof is in the numbers
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            Trusted in production. Proven at scale.
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">
            From one-off research to daily insight pipelines, PodInsight keeps
            your team aligned.
          </p>
          <div className="mt-10 grid gap-6 md:grid-cols-4">
            {stats.map((stat) => (
              <div
                key={stat.label}
                className="rounded-2xl border border-[var(--border)] bg-white p-5"
              >
                <div className="text-3xl font-semibold">{stat.value}</div>
                <div className="mt-2 text-sm text-[var(--ink-muted)]">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / press room
          </div>
          <div className="mt-5 grid gap-6 md:grid-cols-3">
            {press.map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-sm"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
                  {item.outlet}
                </p>
                <h3 className="mt-3 text-lg font-semibold">{item.title}</h3>
                <p className="mt-3 text-sm text-[var(--ink-muted)]">
                  “{item.quote}”
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24 rounded-3xl border border-[var(--border)] bg-[var(--ink)] p-10 text-white">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-white/70">
                / start building
              </div>
              <h2 className="mt-4 text-3xl font-semibold md:text-4xl font-display">
                Power your team with audio-first insights.
              </h2>
              <p className="mt-3 max-w-xl text-white/70">
                Launch your first podcast workflow in minutes. Integrate with
                Slack, Notion, and your internal knowledge base.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button className="rounded-full bg-white px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                Explore API docs
              </button>
              <button className="rounded-full border border-white/30 px-6 py-3 text-sm font-semibold text-white">
                Start free trial
              </button>
            </div>
          </div>
        </section>

        <footer className="mt-24 border-t border-[var(--border)] py-10 text-sm text-[var(--ink-muted)]">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-2 text-base font-semibold text-[var(--ink)]">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--ink)] text-white">
                P
              </span>
              PodInsight
            </div>
            <div className="flex flex-wrap gap-6">
              <span>Company</span>
              <span>Security</span>
              <span>Careers</span>
              <span>Status</span>
              <span>Contact</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
