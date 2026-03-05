from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agents.orchestrator import WarehouseCopilotOrchestrator

app = FastAPI(title="Digital Warehouse Copilot API")
orchestrator = WarehouseCopilotOrchestrator()


class ScenarioRequest(BaseModel):
    scenario: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/run")
def run_workflow(payload: ScenarioRequest) -> dict:
    return orchestrator.run(payload.scenario)
