# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass
from abc import ABC, abstractmethod

if TYPE_CHECKING:
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
