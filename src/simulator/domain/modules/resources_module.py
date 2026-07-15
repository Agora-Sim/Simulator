# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import numpy as np

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass

from .resource import Resource
from .node_module import NodeModule

if TYPE_CHECKING:
    from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ResourcesModule(NodeModule):
    name: ClassVar[str] = "resources_module"

    resources: list[Resource]

    def apply(self, previous_state: SimulationState, rng: np.random.Generator) -> list:
        raise NotImplementedError()
