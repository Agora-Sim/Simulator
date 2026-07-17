# ================================================================
# 0. Section: IMPORTS
# ================================================================
from numpy.typing import NDArray
from dataclasses import dataclass

from .axis import Axis


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricField:
    name: str
    title: str
    x: Axis
    y: Axis
    values: NDArray
    plot_kind: str
