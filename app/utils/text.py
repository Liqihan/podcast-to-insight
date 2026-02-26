from __future__ import annotations


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
