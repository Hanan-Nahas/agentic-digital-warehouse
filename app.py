from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from agents.orchestrator import WarehouseCopilotOrchestrator
from rag.build_index import main as build_index

st.set_page_config(page_title="Agentic Digital Warehouse Copilot", layout="wide")
st.title("Agentic Digital Warehouse Copilot")
st.caption("AI-Powered Spare Parts Intelligence & On-Demand Manufacturing Orchestration")

orchestrator = WarehouseCopilotOrchestrator()

data_dir = Path("data")
st.sidebar.header("Knowledge Base")
if st.sidebar.button("(Re)build Vector Index"):
    build_index()
    st.sidebar.success("Index rebuilt")

uploaded = st.sidebar.file_uploader("Upload extra markdown docs", type=["md", "txt"], accept_multiple_files=True)
if uploaded:
    for f in uploaded:
        (data_dir / f.name).write_bytes(f.read())
    st.sidebar.success(f"Saved {len(uploaded)} files to data/")

st.sidebar.subheader("Available sample docs")
for name in sorted(p.name for p in data_dir.glob("*.md")):
    st.sidebar.write(f"- {name}")

scenario = st.text_area(
    "Enter maintenance scenario",
    "Asset PX-100 has vibration 7.1 mm/s after restart, urgent downtime risk and supplier delay expected.",
    height=120,
)

if st.button("Run Agent Workflow", type="primary"):
    with st.spinner("Running multi-agent workflow..."):
        result = orchestrator.run(scenario)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Work Order Pack (JSON)")
        st.json(result["work_order"])

        st.subheader("Citations")
        for c in result["work_order"]["citations"]:
            st.markdown(f"**{c['doc']}** (`{c['chunk_id']}`)\n\n> {c['snippet']}")

    with col2:
        st.subheader("Metrics")
        st.metric("Total Runtime (ms)", f"{result['metrics']['total_runtime_ms']}")
        st.metric("Token Usage (est.)", result["metrics"]["token_usage_estimate"])
        st.write(result["metrics"]["step_runtime_ms"])

    st.subheader("Trace View")
    for step in result["trace"]:
        with st.expander(f"{step['agent']} ({step['latency_ms']} ms)", expanded=False):
            st.code(json.dumps(step["summary"], indent=2), language="json")
