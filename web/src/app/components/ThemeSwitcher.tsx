"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { useTranslations } from "next-intl";

export default function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const t = useTranslations("Common");

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <label className="flex items-center gap-2 text-xs font-medium text-[var(--ink-muted)]">
      <span className="hidden md:inline">{t("theme.label")}</span>
      <select
        value={mounted ? theme ?? "system" : "system"}
        onChange={(event) => setTheme(event.target.value)}
        className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-3 py-1 text-xs text-[var(--ink)]"
        aria-label={t("theme.label")}
      >
        <option value="light">{t("theme.light")}</option>
        <option value="dark">{t("theme.dark")}</option>
        <option value="system">{t("theme.system")}</option>
      </select>
    </label>
  );
}
