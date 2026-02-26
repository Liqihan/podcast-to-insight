from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_base_url: str
    openai_audio_model: str
    openai_summary_model: str
    http_timeout_s: float
    max_audio_bytes: int
    chunk_chars: int
    chunk_overlap: int
    default_language: str
    default_summary_style: str
    default_max_words: int


def _getenv_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _getenv_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip(
            "/"
        ),
        openai_audio_model=os.getenv("OPENAI_AUDIO_MODEL", "whisper-1"),
        openai_summary_model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
        http_timeout_s=_getenv_float("HTTP_TIMEOUT_S", 120.0),
        max_audio_bytes=_getenv_int("MAX_AUDIO_BYTES", 200 * 1024 * 1024),
        chunk_chars=_getenv_int("SUMMARY_CHUNK_CHARS", 6000),
        chunk_overlap=_getenv_int("SUMMARY_CHUNK_OVERLAP", 300),
        default_language=os.getenv("SUMMARY_LANGUAGE", "zh"),
        default_summary_style=os.getenv("SUMMARY_STYLE", "bullet"),
        default_max_words=_getenv_int("SUMMARY_MAX_WORDS", 200),
    )
