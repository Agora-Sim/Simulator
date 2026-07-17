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
    name: ClassVar[str] = "alive_metric"
    unit: str = "%"
    title: ClassVar[str] = "Alive Metric"

    def calculate(self, state: SimulationState) -> float:
        alive = 0
        dead = 0

        for node in state.nodes:
            if node.status:
                alive += 1
            else:
                dead += 1

        return (alive / (alive + dead)) * 100
