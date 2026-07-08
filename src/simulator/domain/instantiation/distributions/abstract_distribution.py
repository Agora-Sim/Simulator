# ================================================================
# 0. Section: IMPORTS
# ================================================================
from abc import ABC
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class AbstractDistribution(ABC):
    def sample(self, amount: int) -> list[float]:
        raise NotImplementedError("sample method must be implemented")
