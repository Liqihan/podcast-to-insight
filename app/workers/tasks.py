from __future__ import annotations

import asyncio

from app.config import get_settings
from app.services.pipeline import run_pipeline
from app.services.supabase_service import get_supabase_client, update_summary
from app.utils.errors import ServiceError
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.process_episode")
def process_episode_task(summary_id: str, episode_id: int, user_id: str, source_url: str) -> str:
    settings = get_settings()
    try:
        asyncio.run(run_pipeline(settings, summary_id, episode_id, source_url))
    except ServiceError as exc:
        client = get_supabase_client(settings)
        update_summary(
            client,
            summary_id,
            {"status": "failed", "error_message": exc.message},
        )
        raise
    except Exception as exc:
        client = get_supabase_client(settings)
        update_summary(
            client,
            summary_id,
            {"status": "failed", "error_message": str(exc)},
        )
        raise
    return summary_id
