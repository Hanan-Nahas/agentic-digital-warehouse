from __future__ import annotations

from typing import Dict, List

from rag.vector_store import VectorStore


class HybridRetriever:
    def __init__(self):
        self.store = VectorStore()

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, str]]:
        dense_hits = self.store.search(query, k=k)
        query_terms = set(query.lower().split())
        for item in dense_hits:
            text_terms = set(item["text"].lower().split())
            overlap = len(query_terms.intersection(text_terms))
            item["hybrid_score"] = float(item["score"] + overlap / 20)
        return sorted(dense_hits, key=lambda x: x["hybrid_score"], reverse=True)
