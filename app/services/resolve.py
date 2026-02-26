from __future__ import annotations

from html.parser import HTMLParser
import json
import re
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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
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


def _extract_audio_url(html: str) -> str | None:
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


def _extract_audio_from_next_data(html: str) -> str | None:
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


def _find_audio_in_json(node: object) -> str | None:
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
