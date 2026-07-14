# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import numpy as np

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeModule(ABC):
    name: ClassVar[str]
    node_id: int = field(init=False, default=-1)

    @abstractmethod
    def apply(self, previous_state: SimulationState, rng: np.random.Generator) -> list:
        pass
