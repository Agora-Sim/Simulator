# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import ClassVar
from numpy.typing import NDArray
from dataclasses import dataclass

from .connectivity_rule import ConnectivityRule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NormalConnectivity(ConnectivityRule):
    type: ClassVar[str] = "normal"

    @property
    def mean(self) -> float:
        return self.data["mean"]

    @property
    def std(self) -> float:
        return self.data["std"]

    def build(self, id: int, node_row: NDArray) -> np.ndarray:
        return super().build(id, node_row)
