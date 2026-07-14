# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import numpy as np

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass

from .node_module import NodeModule

if TYPE_CHECKING:
    from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MoneyModule(NodeModule):
    name: ClassVar[str] = "money"

    balance: float
    income: float

    def apply(self, previous_state: SimulationState, rng: np.random.Generator) -> list:
        return []
