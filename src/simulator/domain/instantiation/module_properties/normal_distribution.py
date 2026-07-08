# ================================================================
# 0. Section: IMPORTS
# ================================================================
import random

from typing import ClassVar
from dataclasses import dataclass
from .property_distribution import PropertyDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NormalDistribution(PropertyDistribution):
    name: ClassVar[str] = "normal"

    @property
    def mean(self) -> float:
        return self.data["mean"]

    @property
    def std(self) -> float:
        return self.data["std"]

    def sample(self) -> float:
        return random.normalvariate(self.mean, self.std)
