# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

from ...modules import HealthModule, NodeModule
from ...simulation_state import SimulationState
from .module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HealthMetric(ModuleScalarMetric):
    name: ClassVar[str] = "health_metric"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "health"
    unit: str = "%"
    title: ClassVar[str] = "Health Metric"

    def calculate(self, state: SimulationState) -> float:
        return super().calculate(state)
