"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";

export default function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <label className="flex items-center gap-2 text-xs font-medium text-[var(--ink-muted)]">
      <span className="hidden md:inline">主题</span>
      <select
        value={mounted ? theme ?? "system" : "system"}
        onChange={(event) => setTheme(event.target.value)}
        className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-3 py-1 text-xs text-[var(--ink)]"
        aria-label="主题"
      >
        <option value="light">浅色</option>
        <option value="dark">深色</option>
        <option value="system">跟随系统</option>
      </select>
    </label>
  );
}
