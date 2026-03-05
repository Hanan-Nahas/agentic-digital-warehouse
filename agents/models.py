from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentResult:
    name: str
    output: Dict[str, Any]
    latency_ms: float


@dataclass
class WorkflowState:
    user_input: str
    context_docs: List[Dict[str, Any]] = field(default_factory=list)
    extracted: Dict[str, Any] = field(default_factory=dict)
    identified_parts: Dict[str, Any] = field(default_factory=dict)
    make_buy: Dict[str, Any] = field(default_factory=dict)
    estimates: Dict[str, Any] = field(default_factory=dict)
    compliance: Dict[str, Any] = field(default_factory=dict)
    work_order: Dict[str, Any] = field(default_factory=dict)
    traces: List[AgentResult] = field(default_factory=list)

