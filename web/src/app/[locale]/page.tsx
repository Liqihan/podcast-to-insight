"use client";

import { FormEvent, useState } from "react";
import { useTranslations } from "next-intl";
import { useRouter } from "next-intl/navigation";

import { authorizedFetch } from "../lib/api-client";
import LocaleSwitcher from "../components/LocaleSwitcher";
import ThemeSwitcher from "../components/ThemeSwitcher";

const logos = ["Northwind", "Layer9", "Kiteworks", "Studio 11", "Everglow", "Signal Labs"];

type Feature = { title: string; description: string };

type Stat = { value: string; label: string };

type PressItem = { title: string; outlet: string; quote: string };

export default function Home() {
  const router = useRouter();
  const t = useTranslations("Home");
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const features = t.raw("features") as Feature[];
  const stats = t.raw("stats") as Stat[];
  const benchmarks = t.raw("benchmarkLabels") as string[];
  const press = t.raw("pressItems") as PressItem[];

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!url.trim()) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await authorizedFetch<{
        summary_id: string;
        episode_id: number;
      }>("/api/podcast", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      router.push(`/episode/${response.episode_id}?summary_id=${response.summary_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("errors.submitFailed"));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--border)] bg-[var(--panel-translucent)] px-4 py-2 text-xs font-medium text-[var(--ink-muted)] backdrop-blur">
          <div>
            {t("banner.text")} <span className="ml-1 text-[var(--ink)]">{t("banner.action")}</span>
          </div>
          <div className="flex items-center gap-2">
            <LocaleSwitcher />
            <ThemeSwitcher />
          </div>
        </div>

        <header className="mt-6 flex items-center justify-between">
          <div className="flex items-center gap-2 text-base font-semibold">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--accent)] text-white">
              P
            </span>
            {t("brand")}
          </div>
          <nav className="hidden items-center gap-8 text-sm font-medium text-[var(--ink-muted)] md:flex">
            <span className="text-[var(--ink)]">{t("nav.product")}</span>
            <span>{t("nav.pricing")}</span>
            <span>{t("nav.docs")}</span>
            <span>{t("nav.blog")}</span>
          </nav>
          <div className="flex items-center gap-3 text-sm">
            <button className="hidden rounded-full border border-[var(--border)] px-4 py-2 text-[var(--ink)] md:inline-flex">
              {t("actions.login")}
            </button>
            <button className="rounded-full bg-[var(--accent)] px-4 py-2 text-white">
              {t("actions.try")}
            </button>
          </div>
        </header>

        <section className="relative mt-16 overflow-hidden rounded-3xl border border-[var(--border)] bg-[var(--panel-translucent)] p-10 shadow-[0_40px_120px_rgba(20,20,20,0.08)] backdrop-blur">
          <div className="absolute right-[-120px] top-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(255,216,173,0.75),rgba(255,216,173,0))]" />
          <div className="absolute left-[-120px] bottom-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(173,210,255,0.7),rgba(173,210,255,0))]" />
          <div className="relative">
            <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
              {t("hero.kicker")}
            </div>
            <h1 className="mt-6 max-w-2xl text-4xl font-semibold tracking-tight md:text-5xl font-display">
              {t("hero.title")}
            </h1>
            <p className="mt-4 max-w-2xl text-lg text-[var(--ink-muted)]">
              {t("hero.subtitle")}
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <button className="rounded-full bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-white">
                {t("hero.primaryAction")}
              </button>
              <button className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                {t("hero.secondaryAction")}
              </button>
            </div>

            <div className="mt-10 rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-4 shadow-sm">
              <form onSubmit={onSubmit} className="flex flex-col gap-3 md:flex-row md:items-center">
                <input
                  value={url}
                  onChange={(event) => setUrl(event.target.value)}
                  placeholder={t("form.placeholder")}
                  type="url"
                  className="flex h-11 flex-1 items-center rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-4 text-sm text-[var(--ink)]"
                />
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="rounded-full bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-white disabled:opacity-60"
                >
                  {isSubmitting ? t("form.submitting") : t("form.submit")}
                </button>
              </form>
              {error && <div className="mt-3 text-xs text-red-500">{error}</div>}
              <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-[var(--ink-muted)]">
                <span>{t("form.example")}</span>
                <span className="h-1 w-1 rounded-full bg-[var(--ink-muted)]" />
                <span>{t("form.helper")}</span>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-10 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm font-medium text-[var(--ink-muted)]">{t("trustedBy")}</p>
          <div className="flex flex-wrap gap-6 text-sm font-semibold text-[var(--ink-muted)]">
            {logos.map((logo) => (
              <span key={logo}>{logo}</span>
            ))}
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            {t("workflow.kicker")}
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            {t("workflow.title")}
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">{t("workflow.subtitle")}</p>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6 shadow-sm"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--bg-muted)] text-sm font-semibold">
                  {index + 1}
                </div>
                <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
                <p className="mt-2 text-sm text-[var(--ink-muted)]">{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24 rounded-3xl border border-[var(--border)] bg-[var(--panel)] p-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            {t("benchmarksSection.kicker")}
          </div>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
            <h2 className="text-3xl font-semibold tracking-tight md:text-4xl font-display">
              {t("benchmarksSection.title")}
            </h2>
            <button className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-4 py-2 text-sm font-semibold text-[var(--ink)]">
              {t("benchmarksSection.action")}
            </button>
          </div>
          <div className="mt-6 flex flex-wrap gap-3">
            {benchmarks.map((label, index) => (
              <span
                key={label}
                className={`rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.14em] ${
                  index === 0
                    ? "bg-[var(--accent)] text-white"
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
                {t("benchmarksSection.cardPrimary.label")}
              </p>
              <div className="mt-4 text-5xl font-semibold">{t("benchmarksSection.cardPrimary.value")}</div>
              <p className="mt-2 text-sm text-[var(--ink-muted)]">
                {t("benchmarksSection.cardPrimary.description")}
              </p>
            </div>
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                {t("benchmarksSection.cardSecondary.label")}
              </p>
              <div className="mt-4 space-y-3 text-sm text-[var(--ink-muted)]">
                <div className="flex items-center justify-between">
                  <span>{t("benchmarksSection.metrics.speaker")}</span>
                  <span className="font-semibold text-[var(--ink)]">{t("benchmarksSection.metrics.speakerValue")}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>{t("benchmarksSection.metrics.citation")}</span>
                  <span className="font-semibold text-[var(--ink)]">{t("benchmarksSection.metrics.citationValue")}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>{t("benchmarksSection.metrics.topic")}</span>
                  <span className="font-semibold text-[var(--ink)]">{t("benchmarksSection.metrics.topicValue")}</span>
                </div>
              </div>
              <button className="mt-6 w-full rounded-full bg-[var(--accent)] py-3 text-sm font-semibold text-white">
                {t("benchmarksSection.cardSecondary.action")}
              </button>
            </div>
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            {t("proof.kicker")}
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            {t("proof.title")}
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">{t("proof.subtitle")}</p>
          <div className="mt-10 grid gap-6 md:grid-cols-4">
            {stats.map((stat) => (
              <div key={stat.label} className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-5">
                <div className="text-3xl font-semibold">{stat.value}</div>
                <div className="mt-2 text-sm text-[var(--ink-muted)]">{stat.label}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            {t("pressSection.kicker")}
          </div>
          <div className="mt-5 grid gap-6 md:grid-cols-3">
            {press.map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6 shadow-sm"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
                  {item.outlet}
                </p>
                <h3 className="mt-3 text-lg font-semibold">{item.title}</h3>
                <p className="mt-3 text-sm text-[var(--ink-muted)]">“{item.quote}”</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24 rounded-3xl border border-[var(--border)] bg-[var(--accent)] p-10 text-white">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-white/70">
                {t("final.kicker")}
              </div>
              <h2 className="mt-4 text-3xl font-semibold md:text-4xl font-display">
                {t("final.title")}
              </h2>
              <p className="mt-3 max-w-xl text-white/70">{t("final.subtitle")}</p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button className="rounded-full bg-[var(--panel)] px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                {t("final.primaryAction")}
              </button>
              <button className="rounded-full border border-white/30 px-6 py-3 text-sm font-semibold text-white">
                {t("final.secondaryAction")}
              </button>
            </div>
          </div>
        </section>

        <footer className="mt-24 border-t border-[var(--border)] py-10 text-sm text-[var(--ink-muted)]">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-2 text-base font-semibold text-[var(--ink)]">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--accent)] text-white">
                P
              </span>
              {t("brand")}
            </div>
            <div className="flex flex-wrap gap-6">
              <span>{t("footer.company")}</span>
              <span>{t("footer.security")}</span>
              <span>{t("footer.careers")}</span>
              <span>{t("footer.status")}</span>
              <span>{t("footer.contact")}</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
