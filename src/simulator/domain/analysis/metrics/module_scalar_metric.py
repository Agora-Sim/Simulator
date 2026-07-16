# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .metric import Metric
from ...modules import NodeModule
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ModuleScalarMetric(Metric, ABC):
    module: ClassVar[type[NodeModule]]
    attribute: ClassVar[str]

    @abstractmethod
    def calculate(self, state: SimulationState) -> float:
        ages = []
        for node in state.nodes:
            if not node.status:
                continue
            if node.has_module(self.module):
                selected_module = node.get_module(self.module)
                ages.append(getattr(selected_module, self.attribute))

        return sum(ages) / len(ages) if ages else 0.0
