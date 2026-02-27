from __future__ import annotations

import asyncio
from typing import Any

from openai import OpenAI

from app.config import Settings
from app.services.embedding import embed_texts
from app.services.supabase_service import match_podcast_chunks
from app.utils.errors import ServiceError


def _chat_sync(settings: Settings, messages: list[dict[str, str]]) -> str:
    if not settings.openai_api_key:
        raise ServiceError("OPENAI_API_KEY is not set", status_code=501)
    client = OpenAI(base_url=settings.openai_base_url, api_key=settings.openai_api_key)
    try:
        response = client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=messages,
            temperature=0.2,
        )
    except Exception as exc:
        raise ServiceError(f"Chat request failed: {exc}", status_code=502) from exc
    choices = getattr(response, "choices", None)
    if choices:
        content = getattr(choices[0].message, "content", None)
        if content:
            return content.strip()
    raise ServiceError("Empty chat response", status_code=502)


async def generate_rag_answer(
    settings: Settings,
    supabase_client: Any,
    episode_id: int,
    query: str,
    match_threshold: float | None = None,
    match_count: int | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    embeddings = await embed_texts([query], settings)
    query_embedding = embeddings[0] if embeddings else []
    threshold = match_threshold if match_threshold is not None else settings.rag_match_threshold
    count = match_count if match_count is not None else settings.rag_match_count

    matches = match_podcast_chunks(
        supabase_client, query_embedding, threshold, count, episode_id
    )

    context_lines = []
    for idx, match in enumerate(matches, start=1):
        content = match.get("content") or ""
        start_time = match.get("start_time") or 0
        context_lines.append(f"[{idx}] ({start_time:.1f}s) {content}")

    context = "\n\n".join(context_lines)
    system = (
        "You answer questions about podcast episodes using the provided context. "
        "If the context is insufficient, say you don't know."
    )
    user = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer in Chinese."
    answer = await asyncio.to_thread(
        _chat_sync, settings, [{"role": "system", "content": system}, {"role": "user", "content": user}]
    )

    sources = [
        {
            "text": match.get("content"),
            "time": match.get("start_time", 0),
            "similarity": match.get("similarity"),
        }
        for match in matches
    ]
    return answer, sources
