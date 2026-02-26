from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class SummarizeRequest(BaseModel):
    url: HttpUrl
    language: str | None = Field(default=None, min_length=2, max_length=16)
    summary_style: Literal["bullet", "paragraph"] | None = None
    max_words: int | None = Field(default=None, ge=50, le=800)
    include_transcript: bool = False


class SummarizeResponse(BaseModel):
    source_url: HttpUrl
    audio_url: HttpUrl
    summary: str
    transcript: str | None = None
