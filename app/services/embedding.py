from __future__ import annotations

import asyncio

from openai import OpenAI

from app.config import Settings
from app.utils.errors import ServiceError


def _embed_sync(texts: list[str], settings: Settings) -> list[list[float]]:
    if not settings.openai_api_key:
        raise ServiceError("OPENAI_API_KEY is not set", status_code=501)
    client = OpenAI(base_url=settings.openai_base_url, api_key=settings.openai_api_key)
    try:
        response = client.embeddings.create(
            model=settings.openai_embed_model,
            input=texts,
        )
    except Exception as exc:
        raise ServiceError(f"Embedding request failed: {exc}", status_code=502) from exc
    return [item.embedding for item in response.data]


async def embed_texts(texts: list[str], settings: Settings) -> list[list[float]]:
    if not texts:
        return []
    return await asyncio.to_thread(_embed_sync, texts, settings)
