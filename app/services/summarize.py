from __future__ import annotations

import httpx

from app.config import Settings
from app.utils.errors import ServiceError
from app.utils.text import chunk_text


async def _openai_chat(
    settings: Settings, messages: list[dict[str, str]]
) -> str:
    if not settings.openai_api_key:
        raise ServiceError("OPENAI_API_KEY is not set", status_code=501)

    url = f"{settings.openai_base_url}/chat/completions"
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    payload = {
        "model": settings.openai_summary_model,
        "messages": messages,
        "temperature": 0.2,
    }

    try:
        async with httpx.AsyncClient(timeout=settings.http_timeout_s) as client:
            response = await client.post(url, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise ServiceError(f"Summary request failed: {exc}", status_code=502) from exc

    if response.status_code >= 400:
        raise ServiceError(
            f"Summary failed: {response.status_code} {response.text}", status_code=502
        )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise ServiceError("Unexpected summary response format", status_code=502) from exc


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
        return await _openai_chat(settings, messages)

    per_chunk_words = max(80, max_words // len(chunks))
    partials: list[str] = []
    for chunk in chunks:
        messages = _build_prompt(chunk, language, style, per_chunk_words, combine=False)
        partials.append(await _openai_chat(settings, messages))

    combined = "\n\n".join(partials)
    messages = _build_prompt(combined, language, style, max_words, combine=True)
    return await _openai_chat(settings, messages)
