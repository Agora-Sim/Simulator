# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib.axes import Axes
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ....domain.analysis import BaseAggregator



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricRenderer[AggregatorT: BaseAggregator](ABC):
    @abstractmethod
    def draw(self, axes: Axes, series: AggregatorT) -> None: ...
