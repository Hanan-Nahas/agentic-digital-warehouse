from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.vector_store import VectorStore


def main() -> None:
    store = VectorStore()
    store.build("data")
    store.save()
    print(f"Indexed {len(store.metadata)} chunks")


if __name__ == "__main__":
    main()
