# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import ClassVar
from dataclasses import dataclass

from .node_module import NodeModule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HealthModule(NodeModule):
    name: ClassVar[str] = "health"

    health: float
    age: float

    def apply(self, rng: np.random.Generator):
        pass
