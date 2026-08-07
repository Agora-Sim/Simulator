# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

from ...modules import HealthModule, NodeModule
from .distribution_metric import DistributionMetric


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class AgeDistributionMetric(DistributionMetric):
    name: ClassVar[str] = "age_distribution_metric"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "age"
    title: ClassVar[str] = "Age Distribution"
    plot_kind: ClassVar[str] = "heatmap"

    bin_min: float = 0.0
    bin_max: float = 1200.0
    nr_bins: int = 24
