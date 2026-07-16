# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar, cast
from dataclasses import dataclass

from .metric import Metric
from ...modules import HealthModule
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class AgeMetric(Metric):
    name: ClassVar[str] = "age_metric"

    def calculate(self, state: SimulationState) -> float:
        ages = []
        for node in state.nodes:
            if not node.status:
                continue
            if node.has_module(HealthModule):
                health_module = cast(HealthModule, node.get_module(HealthModule))
                ages.append(health_module.age)

        return sum(ages) / len(ages) if ages else 0.0
