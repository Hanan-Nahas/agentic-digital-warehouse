from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from rag.chunker import load_and_chunk_docs
from rag.embedder import LocalEmbedder

VEC_PATH = Path("rag/store/vectors.json")
META_PATH = Path("rag/store/metadata.json")


class VectorStore:
    def __init__(self, embedder: LocalEmbedder | None = None):
        self.embedder = embedder or LocalEmbedder()
        self.metadata: List[Dict[str, str]] = []
        self.vectors: List[List[float]] = []

    def build(self, data_dir: str = "data") -> None:
        chunks = load_and_chunk_docs(data_dir)
        self.vectors = self.embedder.embed_documents([c.text for c in chunks])
        self.metadata = [{"chunk_id": c.chunk_id, "doc": c.doc_name, "text": c.text} for c in chunks]

    def save(self) -> None:
        VEC_PATH.parent.mkdir(parents=True, exist_ok=True)
        VEC_PATH.write_text(json.dumps(self.vectors), encoding="utf-8")
        META_PATH.write_text(json.dumps(self.metadata, indent=2), encoding="utf-8")

    def load(self) -> None:
        self.vectors = json.loads(VEC_PATH.read_text(encoding="utf-8"))
        self.metadata = json.loads(META_PATH.read_text(encoding="utf-8"))

    @staticmethod
    def _dot(a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def search(self, query: str, k: int = 4) -> List[Dict[str, str]]:
        if not (VEC_PATH.exists() and META_PATH.exists()):
            self.build()
            self.save()
        elif not self.vectors:
            self.load()

        q = self.embedder.embed_query(query)
        scored = [(self._dot(v, q), idx) for idx, v in enumerate(self.vectors)]
        scored.sort(key=lambda x: x[0], reverse=True)

        hits: List[Dict[str, str]] = []
        for score, idx in scored[:k]:
            m = self.metadata[idx].copy()
            m["score"] = float(score)
            hits.append(m)
        return hits
