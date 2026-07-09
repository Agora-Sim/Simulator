# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass
from .property_distribution import PropertyDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ConstantDistribution(PropertyDistribution):
    name: ClassVar[str] = "constant"

    @property
    def value(self) -> float:
        return self.data["value"]

    def sample(self) -> float:
        return self.value
