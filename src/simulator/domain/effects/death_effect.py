# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass

from .effect import Effect

if TYPE_CHECKING:
    from ..simulation_state import SimulationState



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class DeathEffect(Effect):
    name: ClassVar[str] = "death"
    priority: ClassVar[int] = 0

    node_id: int

    def apply(self, state: SimulationState) -> None:
        node = next(n for n in state.nodes if n.id == self.node_id)
        node.status = False
