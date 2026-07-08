# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from dataclasses import dataclass

from .distributions import AbstractDistribution, NormalDistribution



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class PropertyDistribution:
    name: str
    data: dict[str, Any]

    @property
    def generator(self) -> AbstractDistribution:
        if self.name == "normal":
            return NormalDistribution(**self.data)
        else:
            raise ValueError(f"Unknown distribution: {self.name}")



    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def sample(self, amount: int) -> list[float]:
        return self.generator.sample(amount)
