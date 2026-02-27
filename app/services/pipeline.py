from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from app.config import Settings
from app.services.download import download_audio
from app.services.embedding import embed_texts
from app.services.resolve import resolve_episode_metadata
from app.services.storage import upload_bytes, upload_file
from app.services.supabase_service import (
    get_supabase_client,
    insert_podcast_chunks,
    update_episode,
    update_summary,
)
from app.services.summarize import summarize_structured
from app.services.transcribe import TranscriptResult, transcribe_file
from app.utils.errors import ServiceError
from app.utils.text import chunk_segments


@dataclass(frozen=True)
class PipelineResult:
    summary_payload: dict[str, Any]
    transcript: TranscriptResult


async def _upload_transcripts(
    settings: Settings,
    client: Any,
    episode_id: int,
    transcript: TranscriptResult,
) -> tuple[str | None, str | None]:
    text_url = None
    json_url = None
    base_path = f"episodes/{episode_id}"
    if transcript.text:
        text_url = upload_bytes(
            client,
            settings,
            transcript.text.encode("utf-8"),
            f"{base_path}/transcript.txt",
            "text/plain; charset=utf-8",
        )
    if transcript.raw:
        json_url = upload_bytes(
            client,
            settings,
            json.dumps(transcript.raw, ensure_ascii=False, indent=2).encode("utf-8"),
            f"{base_path}/transcript.json",
            "application/json; charset=utf-8",
        )
    return text_url, json_url


async def run_pipeline(
    settings: Settings,
    summary_id: str,
    episode_id: int,
    source_url: str,
) -> PipelineResult:
    client = get_supabase_client(settings)
    update_summary(client, summary_id, {"status": "processing"})

    metadata = await resolve_episode_metadata(source_url, settings)
    update_episode(
        client,
        episode_id,
        {
            "title": metadata.title,
            "description": metadata.description,
            "audio_url": metadata.audio_url,
            "cover_image": metadata.cover_image,
            "duration": metadata.duration,
        },
    )

    local_path = None
    try:
        local_path, _ = await download_audio(metadata.audio_url, settings)
        storage_path = f"episodes/{episode_id}/audio{metadata.audio_suffix}"
        audio_url = upload_file(
            client, settings, local_path, storage_path, content_type=metadata.audio_type
        )
        update_episode(client, episode_id, {"storage_path": storage_path, "audio_url": audio_url})

        transcript = await transcribe_file(local_path, settings)
        text_url, json_url = await _upload_transcripts(settings, client, episode_id, transcript)
        if transcript.duration_ms:
            update_episode(client, episode_id, {"duration": int(transcript.duration_ms / 1000)})

        chunks = chunk_segments(
            transcript.segments, settings.transcript_chunk_chars, settings.transcript_chunk_overlap
        )
        embeddings = await embed_texts([chunk["text"] for chunk in chunks], settings)
        chunk_rows = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_rows.append(
                {
                    "episode_id": episode_id,
                    "content": chunk["text"],
                    "start_time": chunk["start_time"],
                    "end_time": chunk["end_time"],
                    "embedding": embedding,
                }
            )
        insert_podcast_chunks(client, chunk_rows)

        summary_payload = await summarize_structured(
            transcript.text,
            settings,
            metadata.language or settings.default_language,
            settings.default_summary_style,
        )

        summary_payload.update(
            {
                "status": "completed",
                "transcript_text_url": text_url,
                "transcript_json_url": json_url,
                "transcript_duration_ms": transcript.duration_ms,
                "asr_model": settings.openai_transcribe_model,
                "summary_model": settings.openai_chat_model,
                "language": metadata.language or settings.default_language,
                "summary_style": settings.default_summary_style,
            }
        )

        update_summary(client, summary_id, summary_payload)
        return PipelineResult(summary_payload=summary_payload, transcript=transcript)
    except ServiceError as exc:
        update_summary(
            client,
            summary_id,
            {"status": "failed", "error_message": exc.message},
        )
        raise
    finally:
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except OSError:
                pass
