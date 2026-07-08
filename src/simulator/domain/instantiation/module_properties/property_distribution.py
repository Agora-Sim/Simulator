# ================================================================
# 0. Section: IMPORTS
# ================================================================
from abc import ABC, abstractmethod
from typing import Any, ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class PropertyDistribution(ABC):
    type: ClassVar[str]
    data: dict[str, Any]

    @abstractmethod
    def sample(self) -> float:
        pass
