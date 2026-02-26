from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.resolve import resolve_audio_url
from app.services.summarize import summarize_text
from app.services.transcribe import transcribe_audio
from app.utils.errors import ServiceError


app = FastAPI(title="Podcast Summarizer", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    settings = get_settings()
    language = request.language or settings.default_language
    style = request.summary_style or settings.default_summary_style
    max_words = request.max_words or settings.default_max_words

    try:
        audio_url = await resolve_audio_url(str(request.url), settings)
        transcript = await transcribe_audio(audio_url, settings)
        summary = await summarize_text(transcript, settings, language, style, max_words)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return SummarizeResponse(
        source_url=request.url,
        audio_url=audio_url,
        summary=summary,
        transcript=transcript if request.include_transcript else None,
    )
