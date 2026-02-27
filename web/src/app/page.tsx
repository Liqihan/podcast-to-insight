"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { authorizedFetch } from "./lib/api-client";
import ThemeSwitcher from "./components/ThemeSwitcher";

const logos = ["Northwind", "Layer9", "Kiteworks", "Studio 11", "Everglow", "Signal Labs"];

const features = [
  {
    title: "即时节目洞察",
    description: "粘贴播客链接，数秒内获得结构化亮点、决策与关键引述。",
  },
  {
    title: "规模化的可靠摘要",
    description: "分段、去重与多轮综合让长音频更准确一致。",
  },
  {
    title: "为团队与工作流打造",
    description: "导出洞察到文档，分享全文转写，并保持音频可追溯。",
  },
];

const stats = [
  { value: "58k+", label: "已处理节目" },
  { value: "3.2x", label: "研究周期更快" },
  { value: "92%", label: "洞察复用率" },
  { value: "24/7", label: "全天候分析" },
];

const benchmarks = ["播客问答", "主题召回", "说话人归因", "长音频摘要"];

const press = [
  {
    title: "几分钟把音频变成行动",
    outlet: "产品评测",
    quote: "这几乎就是播客研究助理：快速、干净，而且稳定得惊人。",
  },
  {
    title: "为深度工作而生的冷静界面",
    outlet: "设计周刊",
    quote: "UI 几乎隐身，让洞察层承担重活。",
  },
  {
    title: "团队的新默认选择",
    outlet: "SaaS Today",
    quote: "播客内容可搜索、可引用、可分享——无需手工转写。",
  },
];

export default function Home() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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
      setError(err instanceof Error ? err.message : "提交失败");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--border)] bg-[var(--panel-translucent)] px-4 py-2 text-xs font-medium text-[var(--ink-muted)] backdrop-blur">
          <div>
            重磅消息：Podcast Insight 已开启内测。{" "}
            <span className="ml-1 text-[var(--ink)]">申请内测 →</span>
          </div>
          <div className="flex items-center gap-2">
            <ThemeSwitcher />
          </div>
        </div>

        <header className="mt-6 flex items-center justify-between">
          <div className="flex items-center gap-2 text-base font-semibold">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[var(--accent)] text-white">
              P
            </span>
            PodInsight
          </div>
          <nav className="hidden items-center gap-8 text-sm font-medium text-[var(--ink-muted)] md:flex">
            <span className="text-[var(--ink)]">产品</span>
            <span>定价</span>
            <span>文档</span>
            <span>博客</span>
          </nav>
          <div className="flex items-center gap-3 text-sm">
            <button className="hidden rounded-full border border-[var(--border)] px-4 py-2 text-[var(--ink)] md:inline-flex">
              登录
            </button>
            <button className="rounded-full bg-[var(--accent)] px-4 py-2 text-white">
              立即体验
            </button>
          </div>
        </header>

        <section className="relative mt-16 overflow-hidden rounded-3xl border border-[var(--border)] bg-[var(--panel-translucent)] p-10 shadow-[0_40px_120px_rgba(20,20,20,0.08)] backdrop-blur">
          <div className="absolute right-[-120px] top-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(255,216,173,0.75),rgba(255,216,173,0))]" />
          <div className="absolute left-[-120px] bottom-[-140px] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(173,210,255,0.7),rgba(173,210,255,0))]" />
          <div className="relative">
            <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
              / 播客洞察层
            </div>
            <h1 className="mt-6 max-w-2xl text-4xl font-semibold tracking-tight md:text-5xl font-display">
              把播客变成可执行的情报。
            </h1>
            <p className="mt-4 max-w-2xl text-lg text-[var(--ink-muted)]">
              将音频连接到你的工作流，提取主题、决策与可引用要点。
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <button className="rounded-full bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-white">
                试用演示
              </button>
              <button className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                咨询专家
              </button>
            </div>

            <div className="mt-10 rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-4 shadow-sm">
              <form onSubmit={onSubmit} className="flex flex-col gap-3 md:flex-row md:items-center">
                <input
                  value={url}
                  onChange={(event) => setUrl(event.target.value)}
                  placeholder="粘贴播客链接"
                  type="url"
                  className="flex h-11 flex-1 items-center rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-4 text-sm text-[var(--ink)]"
                />
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="rounded-full bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-white disabled:opacity-60"
                >
                  {isSubmitting ? "提交中..." : "开始分析"}
                </button>
              </form>
              {error && <div className="mt-3 text-xs text-red-500">{error}</div>}
              <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-[var(--ink-muted)]">
                <span>示例：“嘉宾如何看待 RLHF 安全？”</span>
                <span className="h-1 w-1 rounded-full bg-[var(--ink-muted)]" />
                <span>即时引用与时间戳</span>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-10 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm font-medium text-[var(--ink-muted)]">深受研究者、创始人和媒体团队信赖</p>
          <div className="flex flex-wrap gap-6 text-sm font-semibold text-[var(--ink-muted)]">
            {logos.map((logo) => (
              <span key={logo}>{logo}</span>
            ))}
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / 工作流层
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            研究者喜欢，团队可用。
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">
            从音频到可落地摘要的一切能力，无需手工转写或杂乱文档。
          </p>

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
            / 基准测试
          </div>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
            <h2 className="text-3xl font-semibold tracking-tight md:text-4xl font-display">
              以证据为基础的音频检索。
            </h2>
            <button className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-4 py-2 text-sm font-semibold text-[var(--ink)]">
              查看方法
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
                播客问答得分
              </p>
              <div className="mt-4 text-5xl font-semibold">92.4</div>
              <p className="mt-2 text-sm text-[var(--ink-muted)]">
                覆盖 60+ 小时长音频的一致性摘要。
              </p>
            </div>
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                证据覆盖
              </p>
              <div className="mt-4 space-y-3 text-sm text-[var(--ink-muted)]">
                <div className="flex items-center justify-between">
                  <span>说话人归因</span>
                  <span className="font-semibold text-[var(--ink)]">94%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>引用密度</span>
                  <span className="font-semibold text-[var(--ink)]">87%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>主题覆盖</span>
                  <span className="font-semibold text-[var(--ink)]">91%</span>
                </div>
              </div>
              <button className="mt-6 w-full rounded-full bg-[var(--accent)] py-3 text-sm font-semibold text-white">
                运行你的基准测试
              </button>
            </div>
          </div>
        </section>

        <section className="mt-24">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-muted)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">
            / 以数据为证
          </div>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl font-display">
            生产级可信，规模化验证。
          </h2>
          <p className="mt-4 max-w-2xl text-[var(--ink-muted)]">
            从一次性研究到每日洞察流水线，PodInsight 让团队保持一致。
          </p>
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
            / 媒体报道
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
                / 开始构建
              </div>
              <h2 className="mt-4 text-3xl font-semibold md:text-4xl font-display">
                用音频洞察驱动团队。
              </h2>
              <p className="mt-3 max-w-xl text-white/70">
                几分钟内启动你的首个播客工作流，接入 Slack、Notion 与内部知识库。
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button className="rounded-full bg-[var(--panel)] px-6 py-3 text-sm font-semibold text-[var(--ink)]">
                查看 API 文档
              </button>
              <button className="rounded-full border border-white/30 px-6 py-3 text-sm font-semibold text-white">
                开始免费试用
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
              PodInsight
            </div>
            <div className="flex flex-wrap gap-6">
              <span>公司</span>
              <span>安全</span>
              <span>招聘</span>
              <span>状态</span>
              <span>联系</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
