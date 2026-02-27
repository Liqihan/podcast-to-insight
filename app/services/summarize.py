from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import Any, Optional

import dashscope

from app.config import Settings
from app.utils.errors import ServiceError
from app.utils.text import chunk_text


def _extract_summary_text(output: Any) -> Optional[str]:
    if isinstance(output, dict):
        text = output.get("text")
        if isinstance(text, str) and text.strip():
            return text.strip()
        choices = output.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str) and content.strip():
                        return content.strip()
    return None


def _dashscope_chat_sync(settings: Settings, messages: list[dict[str, str]]) -> str:
    if not settings.dashscope_api_key:
        raise ServiceError("DASHSCOPE_API_KEY is not set", status_code=501)

    dashscope.base_http_api_url = settings.dashscope_base_url
    dashscope.api_key = settings.dashscope_api_key

    response = dashscope.Generation.call(
        model=settings.dashscope_summary_model,
        messages=messages,
        result_format="message",
        temperature=0.2,
    )

    if response.status_code != HTTPStatus.OK:
        raise ServiceError(
            f"Summary failed: {response.code} {response.message}", status_code=502
        )

    text = _extract_summary_text(response.output)
    if not text:
        raise ServiceError("Empty summary result", status_code=502)
    return text


async def _dashscope_chat(
    settings: Settings, messages: list[dict[str, str]]
) -> str:
    return await asyncio.to_thread(_dashscope_chat_sync, settings, messages)


def _build_prompt(
    text: str, language: str, style: str, max_words: int, combine: bool
) -> list[dict[str, str]]:
    system = "You summarize podcast transcripts clearly and accurately."
    if style == "bullet":
        style_instruction = "Use 3-6 bullet points."
    else:
        style_instruction = "Use a single concise paragraph."
    if combine:
        user = (
            "You are given partial summaries from a long transcript. "
            f"Combine, deduplicate, and rewrite a final summary in {language}. "
            f"{style_instruction} Keep it under {max_words} words.\n\nSummaries:\n{text}"
        )
    else:
        user = (
            f"Summarize the following transcript in {language}. {style_instruction} "
            f"Keep it under {max_words} words.\n\nTranscript:\n{text}"
        )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


async def summarize_text(
    text: str, settings: Settings, language: str, style: str, max_words: int
) -> str:
    chunks = chunk_text(text, settings.chunk_chars, settings.chunk_overlap)
    if len(chunks) == 1:
        messages = _build_prompt(chunks[0], language, style, max_words, combine=False)
        return await _dashscope_chat(settings, messages)

    per_chunk_words = max(80, max_words // len(chunks))
    partials: list[str] = []
    for chunk in chunks:
        messages = _build_prompt(chunk, language, style, per_chunk_words, combine=False)
        partials.append(await _dashscope_chat(settings, messages))

    combined = "\n\n".join(partials)
    messages = _build_prompt(combined, language, style, max_words, combine=True)
    return await _dashscope_chat(settings, messages)
