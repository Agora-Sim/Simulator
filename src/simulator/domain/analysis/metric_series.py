# ================================================================
# 0. Section: IMPORTS
# ================================================================
from numpy.typing import NDArray
from dataclasses import dataclass

from .base_aggregator import BaseAggregator


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricSeries(BaseAggregator):
    std: NDArray
