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

    # TODO: Make sure it works with already half-connected nodes
    def build(self, node_id: int, node_row: NDArray) -> np.ndarray:
        size = node_row.shape[0]
        indices = np.random.normal(self.mean, self.std, size)
        indices = np.clip(np.round(indices), 0, size - 1).astype(int)
        row = np.zeros(size)
        row[indices] = 1
        return np.full(node_row.shape, row)
