# SPDX-License-Identifier: MIT
"""
Production Benchmark & Evaluation Suite for LangGraph Workflows.
Measures execution latency, recursion step count, tool calling accuracy,
and state checkpoint integrity across cyclic and multi-agent graphs.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class BenchmarkResult:
    test_name: str
    latency_ms: float
    total_steps: int
    tool_calls_count: int
    success: bool
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentBenchmarkRunner:
    """Evaluates agent graphs against standard reliability benchmarks."""

    def __init__(self, graph_app: Any):
        self.app = graph_app
        self.results: list[BenchmarkResult] = []

    def evaluate_turn(
        self,
        test_name: str,
        initial_input: dict[str, Any],
        config: dict[str, Any],
        validator: Callable[[dict[str, Any]], bool] | None = None,
    ) -> BenchmarkResult:
        start_time = time.perf_counter()
        steps = 0
        tool_count = 0
        final_state: dict[str, Any] = {}

        try:
            for event in self.app.stream(initial_input, config=config):
                steps += 1
                for node_name, state_update in event.items():
                    if "messages" in state_update:
                        for msg in state_update["messages"]:
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                tool_count += len(msg.tool_calls)
                    final_state = state_update

            elapsed = (time.perf_counter() - start_time) * 1000.0
            is_valid = validator(final_state) if validator else True

            result = BenchmarkResult(
                test_name=test_name,
                latency_ms=round(elapsed, 2),
                total_steps=steps,
                tool_calls_count=tool_count,
                success=is_valid,
            )
        except Exception as err:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            result = BenchmarkResult(
                test_name=test_name,
                latency_ms=round(elapsed, 2),
                total_steps=steps,
                tool_calls_count=tool_count,
                success=False,
                metadata={"error": str(err)},
            )

        self.results.append(result)
        return result

    def summary(self) -> dict[str, Any]:
        total = len(self.results)
        if total == 0:
            return {"total_tests": 0, "passed": 0, "pass_rate": "0%"}
        passed = sum(1 for r in self.results if r.success)
        avg_latency = sum(r.latency_ms for r in self.results) / total
        return {
            "total_tests": total,
            "passed": passed,
            "pass_rate": f"{(passed / total) * 100:.1f}%",
            "average_latency_ms": round(avg_latency, 2),
        }
