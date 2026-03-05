from __future__ import annotations

from typing import Dict

from rag.retriever import HybridRetriever

retriever = HybridRetriever()


def run(query: str) -> Dict:
    hits = retriever.retrieve(query, k=6)
    citations = [
        {"doc": h["doc"], "chunk_id": h["chunk_id"], "snippet": h["text"][:220]}
        for h in hits
    ]
    return {"hits": hits, "citations": citations}
