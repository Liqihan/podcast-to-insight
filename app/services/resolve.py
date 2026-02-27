from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import json
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx

from app.config import Settings
from app.utils.errors import ServiceError


AUDIO_EXTENSIONS = (".mp3", ".m4a", ".aac", ".wav", ".ogg", ".flac", ".opus", ".m3u8")


def is_audio_url(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in AUDIO_EXTENSIONS)


class _AudioMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: list[tuple[str, str]] = []
        self.audio_srcs: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, Optional[str]]]
    ) -> None:
        attr_map = {key.lower(): value for key, value in attrs if key}
        if tag.lower() == "meta":
            key = (attr_map.get("property") or attr_map.get("name") or "").lower()
            content = attr_map.get("content")
            if key and content:
                self.meta.append((key, content))
        if tag.lower() == "audio":
            src = attr_map.get("src")
            if src:
                self.audio_srcs.append(src)


@dataclass(frozen=True)
class EpisodeMetadata:
    xyz_id: str
    title: Optional[str]
    description: Optional[str]
    audio_url: str
    cover_image: Optional[str]
    duration: Optional[int]
    audio_suffix: str
    audio_type: str
    language: Optional[str] = None


def _extract_audio_url(html: str) -> Optional[str]:
    parser = _AudioMetaParser()
    parser.feed(html)

    priority_keys = {
        "og:audio",
        "og:audio:secure_url",
        "twitter:player:stream",
        "twitter:player:stream:url",
    }
    for key, content in parser.meta:
        if key in priority_keys:
            return content

    json_audio = _extract_audio_from_next_data(html)
    if json_audio:
        return json_audio

    if parser.audio_srcs:
        return parser.audio_srcs[0]

    match = re.search(
        r"https?://[^\"'\\s>]+\\.(?:mp3|m4a|aac|wav|ogg|flac|opus)(?:\\?[^\"'\\s>]*)?",
        html,
        re.IGNORECASE,
    )
    if match:
        return match.group(0)
    return None


def _extract_audio_from_next_data(html: str) -> Optional[str]:
    match = re.search(
        r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    raw = match.group(1).strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return _find_audio_in_json(data)


def _looks_like_audio_url(value: str) -> bool:
    lower = value.lower()
    if not lower.startswith("http"):
        return False
    if any(ext in lower for ext in AUDIO_EXTENSIONS):
        return True
    if "audio" in lower and "://" in lower:
        return True
    return False


def _find_audio_in_json(node: object) -> Optional[str]:
    if isinstance(node, dict):
        preferred_keys = ("audio", "enclosure", "media", "stream", "source")
        for key in preferred_keys:
            for actual_key, value in node.items():
                if key in actual_key.lower():
                    candidate = _find_audio_in_json(value)
                    if candidate:
                        return candidate

        for key, value in node.items():
            if isinstance(value, str) and _looks_like_audio_url(value):
                return value
            candidate = _find_audio_in_json(value)
            if candidate:
                return candidate
    elif isinstance(node, list):
        for item in node:
            candidate = _find_audio_in_json(item)
            if candidate:
                return candidate
    return None


def _extract_meta(html: str) -> dict[str, str]:
    parser = _AudioMetaParser()
    parser.feed(html)
    meta: dict[str, str] = {}
    for key, content in parser.meta:
        if key and content:
            meta[key] = content
    return meta


def _extract_xyz_id(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return url
    parts = path.split("/")
    return parts[-1]


def _audio_suffix_from_url(url: str) -> str:
    path = urlparse(url).path
    for ext in AUDIO_EXTENSIONS:
        if path.lower().endswith(ext):
            return ext
    return ".bin"


async def resolve_audio_url(url: str, settings: Settings) -> str:
    if is_audio_url(url):
        return url

    headers = {"User-Agent": "podcast-to-insight/0.1"}
    try:
        async with httpx.AsyncClient(
            timeout=settings.http_timeout_s, follow_redirects=True, headers=headers
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.RequestError as exc:
        raise ServiceError(f"Failed to fetch page: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        raise ServiceError(f"Audio page returned {exc.response.status_code}") from exc

    audio_url = _extract_audio_url(response.text)
    if not audio_url:
        raise ServiceError("Unable to locate audio URL on the page", status_code=422)

    return urljoin(str(response.url), audio_url)


async def resolve_episode_metadata(url: str, settings: Settings) -> EpisodeMetadata:
    if is_audio_url(url):
        audio_url = url
        xyz_id = _extract_xyz_id(url)
        suffix = _audio_suffix_from_url(audio_url)
        return EpisodeMetadata(
            xyz_id=xyz_id,
            title=None,
            description=None,
            audio_url=audio_url,
            cover_image=None,
            duration=None,
            audio_suffix=suffix,
            audio_type="audio/mpeg",
        )

    headers = {"User-Agent": "podcast-to-insight/0.1"}
    try:
        async with httpx.AsyncClient(
            timeout=settings.http_timeout_s, follow_redirects=True, headers=headers
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.RequestError as exc:
        raise ServiceError(f"Failed to fetch page: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        raise ServiceError(f"Audio page returned {exc.response.status_code}") from exc

    html = response.text
    audio_url = _extract_audio_url(html)
    if not audio_url:
        raise ServiceError("Unable to locate audio URL on the page", status_code=422)
    audio_url = urljoin(str(response.url), audio_url)

    meta = _extract_meta(html)
    title = meta.get("og:title") or meta.get("twitter:title")
    description = meta.get("og:description") or meta.get("description")
    cover_image = meta.get("og:image") or meta.get("twitter:image")
    language = meta.get("og:locale")
    xyz_id = _extract_xyz_id(str(response.url))
    suffix = _audio_suffix_from_url(audio_url)

    content_type = "audio/mpeg"
    if suffix == ".m4a":
        content_type = "audio/mp4"
    elif suffix == ".aac":
        content_type = "audio/aac"
    elif suffix == ".wav":
        content_type = "audio/wav"
    elif suffix == ".ogg":
        content_type = "audio/ogg"
    elif suffix == ".m3u8":
        content_type = "application/x-mpegURL"

    return EpisodeMetadata(
        xyz_id=xyz_id,
        title=title,
        description=description,
        audio_url=audio_url,
        cover_image=cover_image,
        duration=None,
        audio_suffix=suffix,
        audio_type=content_type,
        language=language,
    )
