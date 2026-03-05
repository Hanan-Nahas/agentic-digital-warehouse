from __future__ import annotations

from typing import Dict

REQUIRED_TOP_LEVEL = [
    "incident_summary",
    "asset",
    "suspected_part",
    "alternatives",
    "recommended_action",
    "manufacturing_feasibility",
    "lead_time_estimate_days",
    "cost_estimate_aed",
    "co2_impact_estimate",
    "risk_flags",
    "citations",
    "next_steps_by_team",
]

ACTIONS = {"DIGITIZE", "SCAN", "REVERSE_ENGINEER", "PRINT", "SOURCE"}


def run(payload: Dict) -> Dict:
    missing = [k for k in REQUIRED_TOP_LEVEL if k not in payload]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    if payload["recommended_action"] not in ACTIONS:
        raise ValueError("Invalid recommended_action")
    for team in ["scanning", "engineering", "qa", "production", "supply_chain"]:
        if team not in payload["next_steps_by_team"]:
            raise ValueError(f"Missing team step: {team}")
    return payload

