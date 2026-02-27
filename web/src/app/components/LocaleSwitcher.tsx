"use client";

import { useTranslations } from "next-intl";
import { useLocale, usePathname, useRouter } from "next-intl/navigation";

import { locales } from "../../i18n";

export default function LocaleSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const t = useTranslations("Common");

  return (
    <label className="flex items-center gap-2 text-xs font-medium text-[var(--ink-muted)]">
      <span className="hidden md:inline">{t("language.label")}</span>
      <select
        value={locale}
        onChange={(event) => router.replace(pathname, { locale: event.target.value })}
        className="rounded-full border border-[var(--border)] bg-[var(--panel)] px-3 py-1 text-xs text-[var(--ink)]"
        aria-label={t("language.label")}
      >
        {locales.map((item) => (
          <option key={item} value={item}>
            {item === "en" ? t("language.english") : t("language.chinese")}
          </option>
        ))}
      </select>
    </label>
  );
}
