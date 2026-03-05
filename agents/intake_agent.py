from __future__ import annotations

import re
from typing import Dict

ASSETS = ["PX-100", "VL-77", "CM-220"]


def run(user_input: str) -> Dict:
    asset = next((a for a in ASSETS if a.lower() in user_input.lower()), "UNKNOWN")
    symptom = user_input.strip()
    constraints = []
    if "urgent" in user_input.lower() or "downtime" in user_input.lower():
        constraints.append("high_urgency")
    if "no oem" in user_input.lower() or "supplier delay" in user_input.lower():
        constraints.append("supplier_unavailable")

    extracted_numbers = re.findall(r"\d+\.?\d*", user_input)
    return {
        "asset": asset,
        "symptom": symptom,
        "constraints": constraints,
        "numbers_observed": extracted_numbers,
    }
