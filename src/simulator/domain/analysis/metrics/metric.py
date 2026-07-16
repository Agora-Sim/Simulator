# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Metric(ABC):
    name: ClassVar[str]
    unit: str
    title: ClassVar[str]

    @abstractmethod
    def calculate(self, state: SimulationState) -> float: ...
