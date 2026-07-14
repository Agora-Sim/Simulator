# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Effect(ABC):
    name: ClassVar[str]
    priority: ClassVar[int]

    @abstractmethod
    def apply(self, state: SimulationState) -> None: ...
