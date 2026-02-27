from __future__ import annotations

import asyncio

from openai import OpenAI

from app.config import Settings
from app.utils.errors import ServiceError
from app.utils.text import chunk_text


def _iflow_chat_sync(settings: Settings, messages: list[dict[str, str]]) -> str:
    if not settings.iflow_api_key:
        raise ServiceError("IFLOW_API_KEY is not set", status_code=501)

    client = OpenAI(base_url=settings.iflow_base_url, api_key=settings.iflow_api_key)
    response = client.chat.completions.create(
        model=settings.iflow_summary_model, messages=messages
    )
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError) as exc:
        raise ServiceError("Unexpected summary response format", status_code=502) from exc
    if not content:
        raise ServiceError("Empty summary result", status_code=502)
    return content.strip()


async def _iflow_chat(settings: Settings, messages: list[dict[str, str]]) -> str:
    return await asyncio.to_thread(_iflow_chat_sync, settings, messages)


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
        return await _iflow_chat(settings, messages)

    per_chunk_words = max(80, max_words // len(chunks))
    partials: list[str] = []
    for chunk in chunks:
        messages = _build_prompt(chunk, language, style, per_chunk_words, combine=False)
        partials.append(await _iflow_chat(settings, messages))

    combined = "\n\n".join(partials)
    messages = _build_prompt(combined, language, style, max_words, combine=True)
    return await _iflow_chat(settings, messages)
