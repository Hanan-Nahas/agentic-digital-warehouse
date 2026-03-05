from __future__ import annotations

import hashlib
from typing import List


class LocalEmbedder:
    """Deterministic lightweight embedder for offline demos (stdlib only)."""

    def __init__(self, dim: int = 256):
        self.dim = dim

    def _embed_text(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        for token in text.lower().split():
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            vec[h % self.dim] += 1.0
        norm = sum(v * v for v in vec) ** 0.5
        return [v / norm for v in vec] if norm else vec

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed_text(text)
