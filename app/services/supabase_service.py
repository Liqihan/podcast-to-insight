from __future__ import annotations

from functools import lru_cache
from typing import Any

from supabase import Client, create_client

from app.config import Settings, get_settings
from app.utils.errors import ServiceError


@lru_cache(maxsize=1)
def _create_supabase_client(settings: Settings) -> Client:
    if not settings.supabase_url or not settings.supabase_service_key:
        raise ServiceError("Supabase settings are not configured", status_code=500)
    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_supabase_client(settings: Settings | None = None) -> Client:
    return _create_supabase_client(settings or get_settings())


def fetch_episode_by_xyz_id(client: Client, xyz_id: str) -> dict[str, Any] | None:
    response = client.table("episodes").select("*").eq("xyz_id", xyz_id).limit(1).execute()
    data = response.data or []
    return data[0] if data else None


def insert_episode(client: Client, payload: dict[str, Any]) -> dict[str, Any]:
    response = client.table("episodes").insert(payload).execute()
    data = response.data or []
    if not data:
        raise ServiceError("Failed to insert episode", status_code=502)
    return data[0]


def update_episode(client: Client, episode_id: int, payload: dict[str, Any]) -> None:
    client.table("episodes").update(payload).eq("id", episode_id).execute()


def insert_summary(client: Client, payload: dict[str, Any]) -> dict[str, Any]:
    response = client.table("summaries").insert(payload).execute()
    data = response.data or []
    if not data:
        raise ServiceError("Failed to insert summary", status_code=502)
    return data[0]


def update_summary(client: Client, summary_id: str, payload: dict[str, Any]) -> None:
    client.table("summaries").update(payload).eq("id", summary_id).execute()


def fetch_summary(client: Client, summary_id: str) -> dict[str, Any] | None:
    response = (
        client.table("summaries").select("*").eq("id", summary_id).limit(1).execute()
    )
    data = response.data or []
    return data[0] if data else None


def fetch_episode(client: Client, episode_id: int) -> dict[str, Any] | None:
    response = client.table("episodes").select("*").eq("id", episode_id).limit(1).execute()
    data = response.data or []
    return data[0] if data else None


def fetch_latest_summary_for_episode(
    client: Client, episode_id: int, user_id: str | None = None
) -> dict[str, Any] | None:
    query = client.table("summaries").select("*").eq("episode_id", episode_id)
    if user_id:
        query = query.eq("user_id", user_id)
    response = query.order("created_at", desc=True).limit(1).execute()
    data = response.data or []
    return data[0] if data else None


def list_user_episodes(client: Client, user_id: str) -> list[dict[str, Any]]:
    response = (
        client.table("summaries")
        .select(
            "id,status,created_at,one_sentence_summary,summary_text,key_takeaways,"
            "episode:episodes(id,xyz_id,title,description,audio_url,storage_path,cover_image,duration,created_at)"
        )
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def insert_podcast_chunks(client: Client, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    client.table("podcast_chunks").insert(rows).execute()


def match_podcast_chunks(
    client: Client,
    query_embedding: list[float],
    match_threshold: float,
    match_count: int,
    episode_id: int,
) -> list[dict[str, Any]]:
    response = client.rpc(
        "match_podcast_chunks",
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count,
            "filter_episode_id": episode_id,
        },
    ).execute()
    return response.data or []


def fetch_completed_summaries_with_episodes(
    client: Client, limit: int
) -> list[dict[str, Any]]:
    response = (
        client.table("summaries")
        .select(
            "id,episode_id,status,summary_text,one_sentence_summary,key_takeaways,"
            "action_items,mind_map_structure,transcript_text_url,transcript_json_url,"
            "created_at,episode:episodes(id,xyz_id,title,description,audio_url,"
            "storage_path,cover_image,duration,created_at)"
        )
        .eq("status", "completed")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []
