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
class MoneyModule(NodeModule):
    name: ClassVar[str] = "money_module"

    balance: float
    income: float

    def apply(self):
        pass
