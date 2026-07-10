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
class ConstantConnectivity(ConnectivityRule):
    type: ClassVar[str] = "constant"

    @property
    def value(self) -> float:
        return self.data["value"]

    # TODO: Make sure it works with already half-connected nodes
    def build(self, node_id: int, node_row: NDArray) -> np.ndarray:
        # make sure the row has value % rows as 1 (position is random)
        num_ones = int(self.value * node_row.shape[0])
        row = np.zeros(node_row.shape[0])
        row[:num_ones] = 1
        np.random.shuffle(row)
        return np.full(node_row.shape, row)
