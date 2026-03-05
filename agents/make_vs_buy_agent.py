from __future__ import annotations

from typing import Dict


def run(part: str, constraints: list[str], retrieval_text: str) -> Dict:
    text = retrieval_text.lower()
    printable = part not in {"SP-PX100-CPL-03"} and "elastomer" not in text
    if "reverse engineer" in text or "scan" in text:
        printable = True

    if "supplier_unavailable" in constraints and printable:
        recommendation = "PRINT"
    elif printable and any(k in text for k in ["lead time > 10", "lane disruption"]):
        recommendation = "REVERSE_ENGINEER"
    elif printable:
        recommendation = "SOURCE"
    else:
        recommendation = "SOURCE"

    if recommendation == "REVERSE_ENGINEER":
        recommendation = "SCAN"

    feasibility = {
        "is_printable": printable,
        "material": "17-4PH" if "impeller" in text or "sp-px100-imp" in part.lower() else "410 SS" if "vl77" in part.lower() else "Unknown",
        "notes": "Local AM feasible after engineering + QA gating." if printable else "Prefer external source due to material/process mismatch.",
    }
    return {"recommended_action": recommendation, "manufacturing_feasibility": feasibility}
