from __future__ import annotations

import asyncio
from http import HTTPStatus
import time
from typing import Any, Optional

import dashscope
from dashscope.audio.asr import Transcription
import httpx

from app.config import Settings
from app.utils.errors import ServiceError


def _extract_transcript(node: Any) -> Optional[str]:
    if isinstance(node, str):
        return node.strip() or None
    if isinstance(node, dict):
        direct = node.get("transcription") or node.get("text")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()

        sentences = node.get("sentences")
        if isinstance(sentences, list):
            sentence_texts = [
                s.get("text")
                for s in sentences
                if isinstance(s, dict) and isinstance(s.get("text"), str)
            ]
            if sentence_texts:
                return " ".join(sentence_texts).strip()

        transcripts = node.get("transcripts")
        if isinstance(transcripts, list):
            transcript_texts: list[str] = []
            for item in transcripts:
                if not isinstance(item, dict):
                    continue
                if isinstance(item.get("text"), str):
                    transcript_texts.append(item["text"])
                    continue
                if isinstance(item.get("transcription"), str):
                    transcript_texts.append(item["transcription"])
            if transcript_texts:
                return "\n".join(transcript_texts).strip()

        results = node.get("results")
        if isinstance(results, list):
            texts: list[str] = []
            for item in results:
                text = _extract_transcript(item)
                if text:
                    texts.append(text)
            if texts:
                return "\n".join(texts)

        for key in ("result", "output", "data"):
            if key in node:
                text = _extract_transcript(node[key])
                if text:
                    return text

    if isinstance(node, list):
        texts = []
        for item in node:
            text = _extract_transcript(item)
            if text:
                texts.append(text)
        if texts:
            return "\n".join(texts)
    return None


def _find_transcription_url(output: Any) -> Optional[str]:
    if isinstance(output, dict):
        results = output.get("results")
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict):
                    url = item.get("transcription_url")
                    if isinstance(url, str) and url.startswith("http"):
                        return url
        for value in output.values():
            url = _find_transcription_url(value)
            if url:
                return url
    elif isinstance(output, list):
        for item in output:
            url = _find_transcription_url(item)
            if url:
                return url
    return None


def _fetch_transcription_json(url: str, settings: Settings) -> Any:
    try:
        with httpx.Client(timeout=settings.http_timeout_s) as client:
            response = client.get(url, follow_redirects=True)
    except httpx.RequestError as exc:
        raise ServiceError(f"Failed to fetch transcription file: {exc}") from exc

    if response.status_code >= 400:
        raise ServiceError(
            f"Transcription file returned {response.status_code}", status_code=502
        )
    try:
        return response.json()
    except ValueError as exc:
        raise ServiceError("Invalid transcription JSON", status_code=502) from exc


def _transcribe_sync(audio_url: str, settings: Settings) -> str:
    if not settings.dashscope_api_key:
        raise ServiceError("DASHSCOPE_API_KEY is not set", status_code=501)

    dashscope.base_http_api_url = settings.dashscope_base_url
    dashscope.api_key = settings.dashscope_api_key

    response = Transcription.async_call(
        model=settings.dashscope_asr_model, file_urls=[audio_url]
    )
    start = time.time()

    while True:
        status = response.output.task_status
        if status in ("SUCCEEDED", "FAILED"):
            break
        if time.time() - start > settings.dashscope_poll_timeout_s:
            raise ServiceError("Transcription timed out", status_code=504)
        time.sleep(settings.dashscope_poll_interval_s)
        response = Transcription.fetch(task=response.output.task_id)

    if response.status_code != HTTPStatus.OK:
        raise ServiceError(
            f"Transcription failed: {response.code} {response.message}",
            status_code=502,
        )

    output = response.output
    transcript = _extract_transcript(output)
    if not transcript:
        transcription_url = _find_transcription_url(output)
        if transcription_url:
            data = _fetch_transcription_json(transcription_url, settings)
            transcript = _extract_transcript(data)
    if not transcript:
        raise ServiceError("Empty transcription result", status_code=502)
    return transcript.strip()


async def transcribe_audio(audio_url: str, settings: Settings) -> str:
    return await asyncio.to_thread(_transcribe_sync, audio_url, settings)
