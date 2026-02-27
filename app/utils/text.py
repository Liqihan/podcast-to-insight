from __future__ import annotations

import json
from typing import Any


def chunk_text(text: str, max_chars: int, overlap: int) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return [""]
    if len(cleaned) <= max_chars:
        return [cleaned]

    overlap = max(0, min(overlap, max_chars // 2))
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + max_chars)
        chunks.append(cleaned[start:end])
        if end >= len(cleaned):
            break
        start = end - overlap
    return chunks


def chunk_segments(
    segments: list[Any], max_chars: int, overlap_chars: int
) -> list[dict[str, Any]]:
    if not segments:
        return []

    normalized = []
    for segment in segments:
        if isinstance(segment, dict):
            text = str(segment.get("text", "")).strip()
            start = float(segment.get("start", 0))
            end = float(segment.get("end", 0))
        else:
            text = str(getattr(segment, "text", "")).strip()
            start = float(getattr(segment, "start", 0))
            end = float(getattr(segment, "end", 0))
        if text:
            normalized.append({"text": text, "start": start, "end": end})

    if not normalized:
        return []

    chunks: list[dict[str, Any]] = []
    i = 0
    while i < len(normalized):
        start_index = i
        chunk_texts: list[str] = []
        total = 0
        while i < len(normalized):
            segment_text = normalized[i]["text"]
            length = len(segment_text)
            if chunk_texts and total + length > max_chars:
                break
            chunk_texts.append(segment_text)
            total += length
            i += 1

        end_index = i - 1
        chunk_content = " ".join(chunk_texts).strip()
        chunks.append(
            {
                "text": chunk_content,
                "start_time": normalized[start_index]["start"],
                "end_time": normalized[end_index]["end"],
            }
        )

        if i >= len(normalized):
            break
        if overlap_chars > 0:
            overlap_total = 0
            j = end_index
            while j >= start_index and overlap_total < overlap_chars:
                overlap_total += len(normalized[j]["text"])
                j -= 1
            i = max(j + 1, start_index + 1)

    return chunks


def extract_json(content: str) -> dict[str, Any] | None:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(content[start : end + 1])
    except json.JSONDecodeError:
        return None
