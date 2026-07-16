# ================================================================
# 0. Section: IMPORTS
# ================================================================
from numpy.typing import NDArray
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricSeries:
    name: str
    title: str
    unit: str
    timepoints: NDArray
    mean: NDArray
    std: NDArray
    time_unit: str
