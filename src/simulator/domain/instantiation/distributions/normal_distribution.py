# ================================================================
# 0. Section: IMPORTS
# ================================================================
import random

from dataclasses import dataclass
from .abstract_distribution import AbstractDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NormalDistribution(AbstractDistribution):
    mean: float
    std: float

    def sample(self, amount: int) -> list[float]:
        return [random.normalvariate(self.mean, self.std) for _ in range(amount)]
