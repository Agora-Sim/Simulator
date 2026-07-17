# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...domain.analysis import Axis, MetricSeries


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricPlot:
    series: MetricSeries

    def render(self) -> Figure:
        figure, axes = plt.subplots()
        self.draw(axes)
        return figure

    def draw(
        self, axes: Axes, show_xlabel: bool = True, show_ylabel: bool = True
    ) -> None:
        """Draw the series onto an existing Axes (used by grids too)."""
        x, y = self.series.x, self.series.y
        axes.plot(x.values, y.values)
        axes.fill_between(
            x.values,
            y.values - self.series.std,
            y.values + self.series.std,
            alpha=0.2,
        )
        axes.set_title(self.series.title)
        if show_xlabel:
            axes.set_xlabel(_axis_label(x))
        if show_ylabel:
            axes.set_ylabel(_axis_label(y))


# ================================================================
# 2. Section: Functions — labelling
# ================================================================
def _axis_label(axis: Axis) -> str:
    return f"{axis.label} ({axis.unit})"
