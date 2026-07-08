# ================================================================
# 0. Section: IMPORTS
# ================================================================

import numpy as np

from typing import ClassVar, Any
from numpy.typing import NDArray
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ================================================================
# 1. Section: Abstract Connectivity Rule
# ================================================================
@dataclass
class ConnectivityRule(ABC):
    data: dict[str, Any]
    type: ClassVar[str]

    @abstractmethod
    def build(self, node_id: int, node_row: NDArray) -> np.ndarray:
        pass
