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

    def build(
        self,
        node_id: int,
        connection_dict: dict[str, list],
        rng: np.random.Generator,
    ) -> NDArray:
        # 1. Extract the data from the connection_dict
        candidates = np.asarray(connection_dict["candidates"])

        return candidates
