from __future__ import annotations

from time import perf_counter
from typing import Any, Dict

from agents import (
    compliance_security_agent,
    estimation_agent,
    intake_agent,
    make_vs_buy_agent,
    parts_identification_agent,
    retrieval_agent,
    work_order_packager_agent,
)
from agents.models import AgentResult, WorkflowState
from agents.utils import timed_run


class WarehouseCopilotOrchestrator:
    def run(self, user_input: str) -> Dict[str, Any]:
        state = WorkflowState(user_input=user_input)
        started = perf_counter()

        intake_out, ms = timed_run(intake_agent.run, user_input)
        state.extracted = intake_out
        state.traces.append(AgentResult("Intake Agent", intake_out, ms))

        query = f"{intake_out['asset']} {intake_out['symptom']} spare part QA reverse engineering"
        ret_out, ms = timed_run(retrieval_agent.run, query)
        state.context_docs = ret_out["hits"]
        state.traces.append(AgentResult("Retrieval Agent", {"top_docs": [h['doc'] for h in ret_out['hits'][:3]]}, ms))

        parts_out, ms = timed_run(
            parts_identification_agent.run,
            intake_out["asset"],
            intake_out["symptom"],
            ret_out["hits"],
        )
        state.identified_parts = parts_out
        state.traces.append(AgentResult("Parts Identification Agent", parts_out, ms))

        retrieval_blob = " ".join([h["text"] for h in ret_out["hits"]])
        make_buy_out, ms = timed_run(
            make_vs_buy_agent.run,
            parts_out["suspected_part"],
            intake_out["constraints"],
            retrieval_blob,
        )
        state.make_buy = make_buy_out
        state.traces.append(AgentResult("Make-vs-Buy Agent", make_buy_out, ms))

        est_out, ms = timed_run(estimation_agent.run, make_buy_out["recommended_action"], parts_out["suspected_part"])
        state.estimates = est_out
        state.traces.append(AgentResult("Estimation Agent", est_out, ms))

        comp_out, ms = timed_run(compliance_security_agent.run, user_input, ret_out["citations"])
        state.compliance = comp_out
        state.traces.append(AgentResult("Compliance & Security Agent", comp_out, ms))

        work_order = {
            "incident_summary": comp_out["sanitized_input"],
            "asset": intake_out["asset"],
            "suspected_part": parts_out["suspected_part"],
            "alternatives": parts_out["alternatives"],
            "recommended_action": make_buy_out["recommended_action"],
            "manufacturing_feasibility": make_buy_out["manufacturing_feasibility"],
            "lead_time_estimate_days": est_out["lead_time_estimate_days"],
            "cost_estimate_aed": est_out["cost_estimate_aed"],
            "co2_impact_estimate": est_out["co2_impact_estimate"],
            "risk_flags": comp_out["risk_flags"],
            "citations": comp_out["safe_citations"],
            "next_steps_by_team": {
                "scanning": ["Capture part geometry and damage map", "Store scan in digital inventory"],
                "engineering": ["Validate tolerances/material", "Approve make-vs-buy decision"],
                "qa": ["Create inspection plan per QA guideline", "Release final conformity report"],
                "production": ["Schedule build or machining slot", "Track completion against downtime window"],
                "supply_chain": ["Raise PO for non-printable items", "Update safety stock and risk status"],
            },
        }

        if comp_out["blocked"]:
            work_order["recommended_action"] = "SOURCE"
            work_order["risk_flags"].append("OUTPUT_RESTRICTED")

        packed, ms = timed_run(work_order_packager_agent.run, work_order)
        state.work_order = packed
        state.traces.append(AgentResult("Work-Order Packager Agent", {"valid_schema": True}, ms))

        total_ms = (perf_counter() - started) * 1000
        metrics = {
            "total_runtime_ms": round(total_ms, 2),
            "step_runtime_ms": {t.name: round(t.latency_ms, 2) for t in state.traces},
            "token_usage_estimate": len(user_input.split()) + sum(len(str(t.output).split()) for t in state.traces),
        }

        trace = [
            {"agent": t.name, "summary": t.output, "latency_ms": round(t.latency_ms, 2)}
            for t in state.traces
        ]

        return {"work_order": packed, "trace": trace, "metrics": metrics}
