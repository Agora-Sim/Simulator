# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from numpy.typing import NDArray
from dataclasses import dataclass

from ..simulation_state import SimulationState
from .metrics import Metric


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricExtractor:
    def extract(self, history: list[SimulationState], metric: Metric) -> NDArray:
        result = []
        for state in history:
            result.append(metric.calculate(state))
        return np.array(result)
