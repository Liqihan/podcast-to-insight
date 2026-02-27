from __future__ import annotations

from datetime import datetime
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


class ProcessRequest(BaseModel):
    url: HttpUrl
    webhook_url: Optional[HttpUrl] = None


class ProcessResponse(BaseModel):
    task_id: str
    summary_id: str
    episode_id: int


class ChatRequest(BaseModel):
    episode_id: int
    query: str = Field(min_length=2)
    match_threshold: Optional[float] = Field(default=None, ge=0, le=1)
    match_count: Optional[int] = Field(default=None, ge=1, le=20)


class ChatSource(BaseModel):
    text: Optional[str] = None
    time: float
    similarity: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]


class StatusResponse(BaseModel):
    summary_id: str
    status: str
    error_message: Optional[str] = None


class EpisodeSummary(BaseModel):
    id: str
    status: str
    summary_text: Optional[str] = None
    one_sentence_summary: Optional[str] = None
    key_takeaways: Optional[list[str]] = None
    action_items: Optional[list[str]] = None
    mind_map_structure: Optional[dict] = None
    transcript_text_url: Optional[str] = None
    transcript_json_url: Optional[str] = None
    created_at: Optional[datetime] = None


class EpisodeResponse(BaseModel):
    id: int
    xyz_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    audio_url: Optional[str] = None
    storage_path: Optional[str] = None
    cover_image: Optional[str] = None
    duration: Optional[int] = None
    created_at: Optional[datetime] = None
    summary: Optional[EpisodeSummary] = None


class UserEpisodeItem(BaseModel):
    summary_id: str
    status: str
    created_at: Optional[datetime] = None
    one_sentence_summary: Optional[str] = None
    summary_text: Optional[str] = None
    key_takeaways: Optional[list[str]] = None
    episode: EpisodeResponse
