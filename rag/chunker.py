from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Chunk:
    chunk_id: str
    doc_name: str
    text: str


def chunk_text(text: str, size: int = 420, overlap: int = 80) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + size)
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks


def load_and_chunk_docs(data_dir: str = "data") -> List[Chunk]:
    path = Path(data_dir)
    docs = sorted(path.glob("*.md"))
    results: List[Chunk] = []
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for idx, part in enumerate(chunk_text(text)):
            results.append(Chunk(chunk_id=f"{doc.stem}-c{idx}", doc_name=doc.name, text=part))
    return results

