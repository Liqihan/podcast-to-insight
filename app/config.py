from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


@dataclass(frozen=True)
class Settings:
    openai_api_key: Optional[str]
    openai_base_url: str
    openai_summary_model: str
    dashscope_api_key: Optional[str]
    dashscope_base_url: str
    dashscope_asr_model: str
    dashscope_poll_interval_s: float
    dashscope_poll_timeout_s: float
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
        openai_summary_model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
        dashscope_base_url=os.getenv(
            "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1"
        ).rstrip("/"),
        dashscope_asr_model=os.getenv("DASHSCOPE_ASR_MODEL", "fun-asr"),
        dashscope_poll_interval_s=_getenv_float("DASHSCOPE_POLL_INTERVAL_S", 2.0),
        dashscope_poll_timeout_s=_getenv_float("DASHSCOPE_POLL_TIMEOUT_S", 900.0),
        http_timeout_s=_getenv_float("HTTP_TIMEOUT_S", 120.0),
        max_audio_bytes=_getenv_int("MAX_AUDIO_BYTES", 200 * 1024 * 1024),
        chunk_chars=_getenv_int("SUMMARY_CHUNK_CHARS", 6000),
        chunk_overlap=_getenv_int("SUMMARY_CHUNK_OVERLAP", 300),
        default_language=os.getenv("SUMMARY_LANGUAGE", "zh"),
        default_summary_style=os.getenv("SUMMARY_STYLE", "bullet"),
        default_max_words=_getenv_int("SUMMARY_MAX_WORDS", 200),
    )
