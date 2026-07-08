# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from dataclasses import dataclass

from .step_type import StepType


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationSpecs:
    data: dict[str, Any]

    @property
    def max_duration(self) -> int:
        return self.data["max_duration"]

    @property
    def re_connection(self) -> bool:
        return self.data["re_connection"]

    @property
    def seed(self) -> int:
        return self.data["seed"]

    @property
    def step_size(self) -> StepType:
        step_type_str = self.data["step_size"]
        return StepType.from_str(step_type_str)
