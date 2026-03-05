from __future__ import annotations

import re
from time import perf_counter
from typing import Any, Callable, Dict

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"bypass policy",
    r"dump all logs",
    r"reveal confidential",
    r"system admin",
]

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{7,}\d")


def detect_prompt_injection(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in INJECTION_PATTERNS)


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    return PHONE_RE.sub("[REDACTED_PHONE]", text)


def timed_run(fn: Callable[..., Dict[str, Any]], *args: Any, **kwargs: Any) -> tuple[Dict[str, Any], float]:
    start = perf_counter()
    out = fn(*args, **kwargs)
    return out, (perf_counter() - start) * 1000
