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
class MoneyModule(NodeModule):
    name: ClassVar[str] = "money"

    balance: float
    income: float

    def apply(self, rng: np.random.Generator):
        pass
