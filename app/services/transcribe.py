from __future__ import annotations

import asyncio
from http import HTTPStatus
import time
from typing import Any, Optional

import dashscope
from dashscope.audio.asr import Transcription

from app.config import Settings
from app.utils.errors import ServiceError


def _extract_transcript(output: Any) -> Optional[str]:
    if isinstance(output, dict):
        if isinstance(output.get("transcription"), str):
            return output["transcription"]
        if isinstance(output.get("text"), str):
            return output["text"]
        results = output.get("results")
        if isinstance(results, list):
            texts: list[str] = []
            for item in results:
                if not isinstance(item, dict):
                    continue
                if isinstance(item.get("transcription"), str):
                    texts.append(item["transcription"])
                    continue
                if isinstance(item.get("text"), str):
                    texts.append(item["text"])
                    continue
                sentences = item.get("sentences")
                if isinstance(sentences, list):
                    sentence_texts = [
                        s.get("text")
                        for s in sentences
                        if isinstance(s, dict) and isinstance(s.get("text"), str)
                    ]
                    if sentence_texts:
                        texts.append(" ".join(sentence_texts))
            if texts:
                return "\n".join(texts)
    return None


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
        raise ServiceError("Empty transcription result", status_code=502)
    return transcript.strip()


async def transcribe_audio(audio_url: str, settings: Settings) -> str:
    return await asyncio.to_thread(_transcribe_sync, audio_url, settings)
