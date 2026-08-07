# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from abc import ABC
from typing import ClassVar
from numpy.typing import NDArray
from dataclasses import dataclass

from .metric import Metric
from ..axis import Axis
from ..metric_field import MetricField
from ...modules import NodeModule
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class DistributionMetric(Metric, ABC):
    module: ClassVar[type[NodeModule]]
    attribute: ClassVar[str]

    bin_min: float = 0.0
    bin_max: float = 100.0
    nr_bins: int = 20

    def __post_init__(self) -> None:
        # A. Declared without values here, so an undeclared subclass fails loudly
        if not hasattr(self, "module") or not hasattr(self, "attribute"):
            raise TypeError(
                f"{type(self).__name__} must declare 'module' and 'attribute'"
            )
        if self.nr_bins < 1:
            raise ValueError("nr_bins must be at least 1")
        if self.bin_max <= self.bin_min:
            raise ValueError("bin_max must be greater than bin_min")

    def calculate(self, state: SimulationState) -> NDArray:
        values = []
        for node in state.nodes:
            if not node.status:
                continue
            if node.has_module(self.module):
                selected_module = node.get_module(self.module)
                values.append(getattr(selected_module, self.attribute))

        counts, _ = np.histogram(
            values, bins=self.nr_bins, range=(self.bin_min, self.bin_max)
        )
        return counts.astype(float)

    def build_result(self, x_axis: Axis, mean: NDArray, std: NDArray) -> MetricField:
        return MetricField(
            name=self.name,
            title=self.title,
            x=x_axis,
            y=Axis(values=self.bin_centres(), label=self.title, unit=self.unit),
            values=mean,
            plot_kind=self.plot_kind,
        )

    def bin_centres(self) -> NDArray:
        edges = np.linspace(self.bin_min, self.bin_max, self.nr_bins + 1)
        return (edges[:-1] + edges[1:]) / 2
