# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from typing import ClassVar

from .metric import Metric
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class AliveMetric(Metric):
    """Percentage of nodes still alive, over all nodes in the state."""

    name: ClassVar[str] = "alive_metric"
    unit: str = "%"
    title: ClassVar[str] = "Alive Metric"

    def calculate(self, state: SimulationState) -> float:
        if not state.nodes:
            return 0.0

        alive = sum(1 for node in state.nodes if node.status)

        return (alive / len(state.nodes)) * 100
