from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas import (
    ChatRequest,
    ChatResponse,
    EpisodeResponse,
    FeaturedEpisodesResponse,
    ProcessRequest,
    ProcessResponse,
    StatusResponse,
    SummarizeRequest,
    SummarizeResponse,
    UserEpisodeItem,
)
from app.services.chat import generate_rag_answer
from app.services.download import convert_audio_to_mp3, download_audio
from app.services.resolve import resolve_audio_url, resolve_episode_metadata
from app.services.summarize import summarize_text
from app.services.supabase_service import (
    fetch_episode,
    fetch_episode_by_xyz_id,
    fetch_latest_summary_for_episode,
    fetch_summary,
    fetch_completed_summaries_with_episodes,
    get_supabase_client,
    insert_episode,
    insert_summary,
    list_user_episodes,
    update_episode,
)
from app.services.transcribe import transcribe_file
from app.utils.auth import UserContext, get_current_user
from app.utils.errors import ServiceError
from app.workers.tasks import process_episode_task


app = FastAPI(title="Podcast Summarizer", version="0.1.0")


@app.exception_handler(ServiceError)
async def service_error_handler(_: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    settings = get_settings()
    language = request.language or settings.default_language
    style = request.summary_style or settings.default_summary_style
    max_words = request.max_words or settings.default_max_words

    local_path = None
    try:
        audio_url = await resolve_audio_url(str(request.url), settings)
        local_path, _ = await download_audio(audio_url, settings)
        converted_path = convert_audio_to_mp3(local_path)
        if converted_path != local_path:
            try:
                import os

                os.remove(local_path)
            except OSError:
                pass
            local_path = converted_path
        transcript = await transcribe_file(local_path, settings)
        summary = await summarize_text(
            transcript.text, settings, language, style, max_words
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    finally:
        if local_path:
            try:
                import os

                os.remove(local_path)
            except OSError:
                pass

    return SummarizeResponse(
        source_url=request.url,
        audio_url=audio_url,
        summary=summary,
        transcript=transcript.text if request.include_transcript else None,
    )


@app.post("/api/v1/process", response_model=ProcessResponse)
async def process_episode(
    request: ProcessRequest, user: UserContext = Depends(get_current_user)
) -> ProcessResponse:
    settings = get_settings()
    try:
        metadata = await resolve_episode_metadata(str(request.url), settings)
        client = get_supabase_client(settings)
        episode = fetch_episode_by_xyz_id(client, metadata.xyz_id)
        episode_payload = {
            "xyz_id": metadata.xyz_id,
            "title": metadata.title,
            "description": metadata.description,
            "audio_url": metadata.audio_url,
            "cover_image": metadata.cover_image,
            "duration": metadata.duration,
        }
        if not episode:
            episode = insert_episode(client, episode_payload)
        else:
            update_episode(client, episode["id"], episode_payload)

        summary = insert_summary(
            client,
            {
                "episode_id": episode["id"],
                "user_id": user.id,
                "status": "pending",
            },
        )
        task = process_episode_task.delay(
            summary["id"], episode["id"], user.id, str(request.url)
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return ProcessResponse(
        task_id=task.id, summary_id=summary["id"], episode_id=episode["id"]
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, user: UserContext = Depends(get_current_user)
) -> ChatResponse:
    settings = get_settings()
    client = get_supabase_client(settings)
    answer, sources = await generate_rag_answer(
        settings,
        client,
        request.episode_id,
        request.query,
        match_threshold=request.match_threshold,
        match_count=request.match_count,
    )
    return ChatResponse(answer=answer, sources=sources)


@app.get("/api/v1/status/{summary_id}", response_model=StatusResponse)
async def summary_status(
    summary_id: str, user: UserContext = Depends(get_current_user)
) -> StatusResponse:
    settings = get_settings()
    client = get_supabase_client(settings)
    summary = fetch_summary(client, summary_id)
    if not summary or summary.get("user_id") != user.id:
        raise HTTPException(status_code=404, detail="Summary not found")
    return StatusResponse(
        summary_id=summary_id,
        status=summary.get("status", "unknown"),
        error_message=summary.get("error_message"),
    )


@app.get("/api/v1/episode/{episode_id}", response_model=EpisodeResponse)
async def episode_detail(
    episode_id: int, user: UserContext = Depends(get_current_user)
) -> EpisodeResponse:
    settings = get_settings()
    client = get_supabase_client(settings)
    episode = fetch_episode(client, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    summary = fetch_latest_summary_for_episode(client, episode_id, user.id)
    episode["summary"] = summary
    return EpisodeResponse.model_validate(episode)


@app.get("/api/v1/user/episodes", response_model=list[UserEpisodeItem])
async def user_episodes(
    user: UserContext = Depends(get_current_user),
) -> list[UserEpisodeItem]:
    settings = get_settings()
    client = get_supabase_client(settings)
    rows = list_user_episodes(client, user.id)
    items: list[UserEpisodeItem] = []
    for row in rows:
        episode_data = row.get("episode") or {}
        items.append(
            UserEpisodeItem(
                summary_id=row.get("id"),
                status=row.get("status"),
                created_at=row.get("created_at"),
                one_sentence_summary=row.get("one_sentence_summary"),
                summary_text=row.get("summary_text"),
                key_takeaways=row.get("key_takeaways"),
                episode=EpisodeResponse.model_validate(episode_data),
            )
        )
    return items


@app.get("/api/v1/episodes/featured", response_model=FeaturedEpisodesResponse)
async def featured_episodes(limit: int = 6) -> FeaturedEpisodesResponse:
    limit = max(1, min(20, int(limit)))
    scan_limit = max(limit * 20, 100)
    scan_limit = min(scan_limit, 500)

    settings = get_settings()
    client = get_supabase_client(settings)
    rows = fetch_completed_summaries_with_episodes(client, scan_limit)

    latest: list[EpisodeResponse] = []
    latest_seen: set[int] = set()

    counts: dict[int, int] = {}
    latest_row_by_episode: dict[int, dict] = {}
    latest_index_by_episode: dict[int, int] = {}

    for idx, row in enumerate(rows):
        episode_id = row.get("episode_id")
        if not episode_id:
            continue
        counts[episode_id] = counts.get(episode_id, 0) + 1
        if episode_id not in latest_row_by_episode:
            latest_row_by_episode[episode_id] = row
            latest_index_by_episode[episode_id] = idx

        if episode_id in latest_seen:
            continue
        episode = row.get("episode") or {}
        if not episode:
            continue
        summary_payload = {
            "id": row.get("id"),
            "status": row.get("status"),
            "summary_text": row.get("summary_text"),
            "one_sentence_summary": row.get("one_sentence_summary"),
            "key_takeaways": row.get("key_takeaways"),
            "action_items": row.get("action_items"),
            "mind_map_structure": row.get("mind_map_structure"),
            "transcript_text_url": row.get("transcript_text_url"),
            "transcript_json_url": row.get("transcript_json_url"),
            "created_at": row.get("created_at"),
        }
        episode_payload = dict(episode)
        episode_payload["summary"] = summary_payload
        latest.append(EpisodeResponse.model_validate(episode_payload))
        latest_seen.add(episode_id)
        if len(latest) >= limit:
            break

    hot_ids = sorted(
        counts.keys(),
        key=lambda episode_id: (
            -counts[episode_id],
            latest_index_by_episode.get(episode_id, 10**9),
        ),
    )
    hot: list[EpisodeResponse] = []
    for episode_id in hot_ids:
        row = latest_row_by_episode.get(episode_id)
        if not row:
            continue
        episode = row.get("episode") or {}
        if not episode:
            continue
        summary_payload = {
            "id": row.get("id"),
            "status": row.get("status"),
            "summary_text": row.get("summary_text"),
            "one_sentence_summary": row.get("one_sentence_summary"),
            "key_takeaways": row.get("key_takeaways"),
            "action_items": row.get("action_items"),
            "mind_map_structure": row.get("mind_map_structure"),
            "transcript_text_url": row.get("transcript_text_url"),
            "transcript_json_url": row.get("transcript_json_url"),
            "created_at": row.get("created_at"),
        }
        episode_payload = dict(episode)
        episode_payload["summary"] = summary_payload
        hot.append(EpisodeResponse.model_validate(episode_payload))
        if len(hot) >= limit:
            break

    return FeaturedEpisodesResponse(latest=latest, hot=hot)
