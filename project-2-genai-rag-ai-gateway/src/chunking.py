"""Split public regulatory text into overlapping chunks for a vector index.

No model call. Safe to unit test. The embedding step is a separate job that
uses a Foundation Model API embedding endpoint once Unity Catalog exists.
"""

from __future__ import annotations


def chunk_text(text: str, size: int = 800, overlap: int = 120) -> list[str]:
    if size <= overlap:
        raise ValueError("size must be greater than overlap")
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = end - overlap
    return chunks
