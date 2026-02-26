from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl


class SummarizeRequest(BaseModel):
    url: HttpUrl
    language: Optional[str] = Field(default=None, min_length=2, max_length=16)
    summary_style: Optional[Literal["bullet", "paragraph"]] = None
    max_words: Optional[int] = Field(default=None, ge=50, le=800)
    include_transcript: bool = False


class SummarizeResponse(BaseModel):
    source_url: HttpUrl
    audio_url: HttpUrl
    summary: str
    transcript: Optional[str] = None
