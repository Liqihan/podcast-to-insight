from __future__ import annotations

import asyncio

from openai import OpenAI

from app.config import Settings
from app.utils.errors import ServiceError
from app.utils.text import chunk_text, extract_json


def _chat_sync(settings: Settings, messages: list[dict[str, str]]) -> str:
    if not settings.bailian_api_key:
        raise ServiceError("BAILIAN_API_KEY is not set", status_code=501)

    client = OpenAI(base_url=settings.bailian_base_url, api_key=settings.bailian_api_key)
    try:
        response = client.chat.completions.create(
            model=settings.bailian_chat_model,
            messages=messages,
            temperature=0.3,
            max_tokens=settings.openai_summary_max_tokens,
        )
    except Exception as exc:
        raise ServiceError(f"Summary request failed: {exc}", status_code=502) from exc

    choices = getattr(response, "choices", None)
    if choices and len(choices) > 0:
        content = getattr(choices[0].message, "content", None)
        if content:
            return content.strip()

    raise ServiceError("Empty summary result", status_code=502)


async def _chat(settings: Settings, messages: list[dict[str, str]]) -> str:
    return await asyncio.to_thread(_chat_sync, settings, messages)


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
        return await _chat(settings, messages)

    per_chunk_words = max(80, max_words // len(chunks))
    partials: list[str] = []
    for chunk in chunks:
        messages = _build_prompt(chunk, language, style, per_chunk_words, combine=False)
        partials.append(await _chat(settings, messages))

    combined = "\n\n".join(partials)
    messages = _build_prompt(combined, language, style, max_words, combine=True)
    return await _chat(settings, messages)


async def summarize_structured(
    text: str, settings: Settings, language: str, style: str
) -> dict[str, object]:
    source_text = text
    if len(text) > settings.chunk_chars:
        source_text = await summarize_text(
            text, settings, language, style, settings.default_max_words
        )
    system = (
        "You summarize podcast transcripts and return strict JSON with keys: "
        "one_sentence_summary, summary_text, key_takeaways, action_items, mind_map_structure."
    )
    style_instruction = "Use bullet points." if style == "bullet" else "Use a paragraph."
    user = (
        f"Summarize the following transcript in {language}. {style_instruction}\n"
        "Return JSON only.\n\nTranscript:\n"
        f"{source_text}"
    )
    content = await _chat(settings, [{"role": "system", "content": system}, {"role": "user", "content": user}])
    payload = extract_json(content) or {}
    if not payload:
        return {
            "summary_text": content,
            "one_sentence_summary": None,
            "key_takeaways": None,
            "action_items": None,
            "mind_map_structure": None,
            "summary_json": None,
        }

    summary_text = payload.get("summary_text") or payload.get("summary") or content
    return {
        "summary_text": summary_text,
        "one_sentence_summary": payload.get("one_sentence_summary"),
        "key_takeaways": payload.get("key_takeaways"),
        "action_items": payload.get("action_items"),
        "mind_map_structure": payload.get("mind_map_structure"),
        "summary_json": payload,
    }
