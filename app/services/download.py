from __future__ import annotations

import os
import tempfile
from urllib.parse import urlparse

import httpx

from app.config import Settings
from app.utils.errors import ServiceError


def _suffix_from_url(url: str) -> str:
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext if ext else ".bin"


async def download_audio(url: str, settings: Settings) -> tuple[str, int]:
    suffix = _suffix_from_url(url)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    total = 0
    try:
        async with httpx.AsyncClient(
            timeout=settings.http_timeout_s, follow_redirects=True
        ) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                content_length = response.headers.get("Content-Length")
                if content_length:
                    try:
                        length_value = int(content_length)
                    except ValueError:
                        length_value = None
                    if length_value and length_value > settings.max_audio_bytes:
                        raise ServiceError("Audio file is too large", status_code=413)
                async for chunk in response.aiter_bytes():
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > settings.max_audio_bytes:
                        raise ServiceError("Audio file is too large", status_code=413)
                    tmp_file.write(chunk)
    except httpx.RequestError as exc:
        try:
            os.remove(tmp_file.name)
        except OSError:
            pass
        raise ServiceError(f"Failed to download audio: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        try:
            os.remove(tmp_file.name)
        except OSError:
            pass
        raise ServiceError(
            f"Audio URL returned {exc.response.status_code}", status_code=502
        ) from exc
    except Exception:
        try:
            os.remove(tmp_file.name)
        except OSError:
            pass
        raise
    finally:
        tmp_file.close()

    if total == 0:
        try:
            os.remove(tmp_file.name)
        except OSError:
            pass
        raise ServiceError("Downloaded audio was empty", status_code=502)

    return tmp_file.name, total
