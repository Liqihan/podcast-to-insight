from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


@dataclass(frozen=True)
class Settings:
    supabase_url: Optional[str]
    supabase_service_key: Optional[str]
    supabase_jwt_secret: Optional[str]
    supabase_storage_bucket: str
    bailian_api_key: Optional[str]
    bailian_base_url: str
    bailian_chat_model: str
    bailian_transcribe_model: str
    bailian_asr_api_key: Optional[str]
    bailian_asr_base_url: str
    bailian_asr_model: str
    bailian_poll_interval_s: float
    bailian_poll_timeout_s: float
    openai_api_key: Optional[str]
    openai_base_url: str
    openai_chat_model: str
    openai_embed_model: str
    openai_transcribe_model: str
    openai_summary_max_tokens: int
    celery_broker_url: Optional[str]
    celery_result_backend: Optional[str]
    redis_url: Optional[str]
    rag_match_threshold: float
    rag_match_count: int
    dashscope_api_key: Optional[str]
    dashscope_base_url: str
    dashscope_asr_model: str
    dashscope_poll_interval_s: float
    dashscope_poll_timeout_s: float
    iflow_api_key: Optional[str]
    iflow_base_url: str
    iflow_summary_model: str
    http_timeout_s: float
    max_audio_bytes: int
    chunk_chars: int
    chunk_overlap: int
    transcript_chunk_chars: int
    transcript_chunk_overlap: int
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
    bailian_transcribe_model = os.getenv("BAILIAN_TRANSCRIBE_MODEL")
    if not bailian_transcribe_model:
        bailian_transcribe_model = os.getenv("BAILIAN_ASR_MODEL", "paraformer-realtime-v2")
    return Settings(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_service_key=os.getenv("SUPABASE_SERVICE_KEY"),
        supabase_jwt_secret=os.getenv("SUPABASE_JWT_SECRET"),
        supabase_storage_bucket=os.getenv("SUPABASE_STORAGE_BUCKET", "podcasts"),
        bailian_api_key=os.getenv("BAILIAN_API_KEY"),
        bailian_base_url=os.getenv("BAILIAN_BASE_URL", "https://bailian.aliyuncs.com/v1").rstrip(
            "/"
        ),
        bailian_chat_model=os.getenv("BAILIAN_CHAT_MODEL", "qwen-plus"),
        bailian_transcribe_model=bailian_transcribe_model,
        bailian_asr_api_key=os.getenv("BAILIAN_ASR_API_KEY"),
        bailian_asr_base_url=os.getenv(
            "BAILIAN_ASR_BASE_URL", "https://nls-gateway-cn-shanghai.aliyuncs.com"
        ).rstrip("/"),
        bailian_asr_model=os.getenv("BAILIAN_ASR_MODEL", "paraformer-realtime-v2"),
        bailian_poll_interval_s=_getenv_float("BAILIAN_POLL_INTERVAL_S", 2.0),
        bailian_poll_timeout_s=_getenv_float("BAILIAN_POLL_TIMEOUT_S", 900.0),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip(
            "/"
        ),
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        openai_embed_model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
        openai_transcribe_model=os.getenv("OPENAI_TRANSCRIBE_MODEL", "whisper-1"),
        openai_summary_max_tokens=_getenv_int("OPENAI_SUMMARY_MAX_TOKENS", 800),
        celery_broker_url=os.getenv("CELERY_BROKER_URL"),
        celery_result_backend=os.getenv("CELERY_RESULT_BACKEND"),
        redis_url=os.getenv("REDIS_URL"),
        rag_match_threshold=_getenv_float("RAG_MATCH_THRESHOLD", 0.2),
        rag_match_count=_getenv_int("RAG_MATCH_COUNT", 5),
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
        dashscope_base_url=os.getenv(
            "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1"
        ).rstrip("/"),
        dashscope_asr_model=os.getenv("DASHSCOPE_ASR_MODEL", "fun-asr"),
        dashscope_poll_interval_s=_getenv_float("DASHSCOPE_POLL_INTERVAL_S", 2.0),
        dashscope_poll_timeout_s=_getenv_float("DASHSCOPE_POLL_TIMEOUT_S", 900.0),
        iflow_api_key=os.getenv("IFLOW_API_KEY"),
        iflow_base_url=os.getenv("IFLOW_BASE_URL", "https://apis.iflow.cn/v1").rstrip(
            "/"
        ),
        iflow_summary_model=os.getenv("IFLOW_SUMMARY_MODEL", "qwen3-max"),
        http_timeout_s=_getenv_float("HTTP_TIMEOUT_S", 120.0),
        max_audio_bytes=_getenv_int("MAX_AUDIO_BYTES", 200 * 1024 * 1024),
        chunk_chars=_getenv_int("SUMMARY_CHUNK_CHARS", 6000),
        chunk_overlap=_getenv_int("SUMMARY_CHUNK_OVERLAP", 300),
        transcript_chunk_chars=_getenv_int("TRANSCRIPT_CHUNK_CHARS", 2000),
        transcript_chunk_overlap=_getenv_int("TRANSCRIPT_CHUNK_OVERLAP", 200),
        default_language=os.getenv("SUMMARY_LANGUAGE", "zh"),
        default_summary_style=os.getenv("SUMMARY_STYLE", "bullet"),
        default_max_words=_getenv_int("SUMMARY_MAX_WORDS", 200),
    )
