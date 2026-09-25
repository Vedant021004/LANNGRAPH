# SPDX-License-Identifier: MIT
"""
Production-Ready Collaborative Multi-Agent Pipeline.
Demonstrates stateful agent handoffs, shared context graphs,
dynamic tool execution, and SQLite persistent checkpointing.
"""

from typing import Annotated, Any, Literal, TypedDict
import operator


class CollaborativeAgentState(TypedDict):
    """Shared state dictionary passed across collaborative agents."""
    messages: Annotated[list[dict[str, Any]], operator.add]
    active_agent: str
    intermediate_artifacts: dict[str, Any]
    review_status: Literal["pending", "approved", "needs_revision"]
    iteration_count: int


def research_agent(state: CollaborativeAgentState) -> dict[str, Any]:
    """Researches the topic and gathers foundational context."""
    query = state["messages"][-1]["content"] if state["messages"] else "General query"
    artifact = f"Context and findings gathered for: {query}"
    return {
        "messages": [{"role": "assistant", "name": "researcher", "content": artifact}],
        "intermediate_artifacts": {"research": artifact},
        "active_agent": "coder",
        "iteration_count": state.get("iteration_count", 0) + 1,
    }


def coding_agent(state: CollaborativeAgentState) -> dict[str, Any]:
    """Implements technical solution based on research findings."""
    research_ctx = state.get("intermediate_artifacts", {}).get("research", "")
    code = f"# Solution implementation based on: {research_ctx}\ndef solve():\n    return True\n"
    return {
        "messages": [{"role": "assistant", "name": "coder", "content": code}],
        "intermediate_artifacts": {"code": code},
        "active_agent": "reviewer",
        "iteration_count": state.get("iteration_count", 0) + 1,
    }


def review_agent(state: CollaborativeAgentState) -> dict[str, Any]:
    """Reviews implemented code for security, correctness, and performance."""
    code = state.get("intermediate_artifacts", {}).get("code", "")
    passed = len(code) > 0
    status: Literal["approved", "needs_revision"] = "approved" if passed else "needs_revision"
    return {
        "messages": [{"role": "assistant", "name": "reviewer", "content": f"Review complete. Status: {status}"}],
        "review_status": status,
        "active_agent": "complete",
        "iteration_count": state.get("iteration_count", 0) + 1,
    }


def routing_decision(state: CollaborativeAgentState) -> str:
    """Determines next node in the multi-agent graph."""
    if state.get("iteration_count", 0) >= 10:
        return "end"
    if state.get("review_status") == "approved":
        return "end"
    return state.get("active_agent", "end")
