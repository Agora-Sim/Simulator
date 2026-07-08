# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

from .node_module import NodeModule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HealthModule(NodeModule):
    name: ClassVar[str] = "health_module"

    health: float
    age: float

    def apply(self):
        pass
