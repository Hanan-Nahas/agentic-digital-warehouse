from __future__ import annotations

from typing import Dict, List


RULES = [
    ("vibration", "PX-100", "SP-PX100-CPL-03", ["SP-PX90-CPL-09", "SP-PX100-IMP-01"]),
    ("seal leak", "PX-100", "SP-PX100-SEAL-07", ["SP-PX100-IMP-01"]),
    ("valve stuck", "VL-77", "SP-VL77-STEM-04", ["Machine from 410 SS bar"]),
    ("compressor noise", "CM-220", "SP-CM220-VLV-11", ["SP-CM220-RING-02"]),
]


def run(asset: str, symptom: str, retrieved_hits: List[Dict]) -> Dict:
    symptom_l = symptom.lower()
    suspected = "UNKNOWN-PART"
    alternatives: List[str] = []

    for key, asset_rule, part, alts in RULES:
        if key in symptom_l and (asset == asset_rule or asset == "UNKNOWN"):
            suspected = part
            alternatives = alts
            break

    if suspected == "UNKNOWN-PART":
        for hit in retrieved_hits:
            txt = hit["text"]
            if "SP-" in txt:
                token = next((w.strip(".,)") for w in txt.split() if w.startswith("SP-")), "UNKNOWN-PART")
                suspected = token
                break

    specs = {
        "criticality": "High" if suspected in ["SP-PX100-IMP-01", "SP-VL77-STEM-04", "SP-CM220-VLV-11"] else "Medium",
        "required_checks": ["material verification", "dimensional validation", "fit-up check"],
    }

    return {"suspected_part": suspected, "alternatives": alternatives, "specs": specs}
