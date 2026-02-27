from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any

from supabase import Client

from app.config import Settings
from app.utils.errors import ServiceError


def _guess_content_type(path: str) -> str:
    content_type, _ = mimetypes.guess_type(path)
    return content_type or "application/octet-stream"


def upload_file(
    client: Client,
    settings: Settings,
    local_path: str,
    remote_path: str,
    content_type: str | None = None,
) -> str:
    bucket = client.storage.from_(settings.supabase_storage_bucket)
    file_path = Path(local_path)
    if not file_path.exists():
        raise ServiceError(f"File not found: {local_path}", status_code=500)

    payload = file_path.read_bytes()
    options: dict[str, Any] = {
        "content-type": content_type or _guess_content_type(local_path),
        "upsert": True,
    }
    bucket.upload(remote_path, payload, file_options=options)
    return bucket.get_public_url(remote_path)


def upload_bytes(
    client: Client,
    settings: Settings,
    content: bytes,
    remote_path: str,
    content_type: str,
) -> str:
    bucket = client.storage.from_(settings.supabase_storage_bucket)
    options: dict[str, Any] = {"content-type": content_type, "upsert": True}
    bucket.upload(remote_path, content, file_options=options)
    return bucket.get_public_url(remote_path)
