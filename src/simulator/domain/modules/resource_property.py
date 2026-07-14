# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from abc import ABC
from typing import ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ResourceProperty(ABC):
    name: ClassVar[str]

    def apply(self, rng: np.random.Generator):
        raise NotImplementedError("apply method must be implemented")
