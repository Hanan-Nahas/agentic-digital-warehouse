from __future__ import annotations

from typing import Dict, List

from agents.utils import detect_prompt_injection, redact_pii


def run(user_input: str, citations: List[Dict]) -> Dict:
    risk_flags: List[str] = []
    blocked = False

    if detect_prompt_injection(user_input):
        risk_flags.append("PROMPT_INJECTION_ATTEMPT")
        blocked = True

    sanitized_input = redact_pii(user_input)

    safe_citations = []
    for c in citations:
        snippet = redact_pii(c["snippet"])
        if "Confidential-IP" in snippet:
            risk_flags.append("IP_SENSITIVE_CONTENT")
            snippet = "[REDACTED_IP_CONTENT]"
        safe_citations.append({**c, "snippet": snippet})

    return {
        "blocked": blocked,
        "risk_flags": sorted(set(risk_flags)),
        "sanitized_input": sanitized_input,
        "safe_citations": safe_citations,
    }
