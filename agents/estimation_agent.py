from __future__ import annotations

from typing import Dict


def run(action: str, part: str) -> Dict:
    if action in {"PRINT", "SCAN", "REVERSE_ENGINEER"}:
        lead_days = 4 if "CPL" in part else 7
        cost = 8500 if "IMP" in part else 6200
        co2 = "Estimated 11 kg CO2e/kg equivalent via local AM + short-haul logistics"
    else:
        lead_days = 18
        cost = 5600
        co2 = "Estimated 32 kg CO2e/kg equivalent via imported sourcing + air freight"

    return {
        "lead_time_estimate_days": float(lead_days),
        "cost_estimate_aed": float(cost),
        "co2_impact_estimate": co2,
    }
