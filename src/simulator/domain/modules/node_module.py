# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from abc import ABC, abstractmethod
from typing import ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeModule(ABC):
    name: ClassVar[str]

    @abstractmethod
    def apply(self, rng: np.random.Generator):
        pass
