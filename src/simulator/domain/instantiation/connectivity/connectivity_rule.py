# ================================================================
# 0. Section: IMPORTS
# ================================================================

import numpy as np

from typing import ClassVar, Any
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
    def build(
        self,
        node_id: int,
        connection_dict: dict[str, list],
        rng: np.random.Generator,
    ) -> np.ndarray:
        pass
