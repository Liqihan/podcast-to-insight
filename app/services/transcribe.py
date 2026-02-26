from __future__ import annotations

import os

import httpx

from app.config import Settings
from app.utils.errors import ServiceError


async def transcribe_audio(file_path: str, settings: Settings) -> str:
    if not settings.openai_api_key:
        raise ServiceError("OPENAI_API_KEY is not set", status_code=501)

    url = f"{settings.openai_base_url}/audio/transcriptions"
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    data = {"model": settings.openai_audio_model, "response_format": "text"}

    try:
        async with httpx.AsyncClient(timeout=settings.http_timeout_s) as client:
            with open(file_path, "rb") as handle:
                files = {
                    "file": (
                        os.path.basename(file_path),
                        handle,
                        "application/octet-stream",
                    )
                }
                response = await client.post(url, headers=headers, data=data, files=files)
    except httpx.RequestError as exc:
        raise ServiceError(f"Transcription request failed: {exc}", status_code=502) from exc

    if response.status_code >= 400:
        raise ServiceError(
            f"Transcription failed: {response.status_code} {response.text}",
            status_code=502,
        )

    transcript = response.text.strip()
    if not transcript:
        raise ServiceError("Empty transcription result", status_code=502)
    return transcript
