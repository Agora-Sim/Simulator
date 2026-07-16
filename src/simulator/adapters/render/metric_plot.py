# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...domain.analysis import MetricSeries


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
        axes.plot(self.series.timepoints, self.series.mean)
        axes.fill_between(
            self.series.timepoints,
            self.series.mean - self.series.std,
            self.series.mean + self.series.std,
            alpha=0.2,
        )
        axes.set_title(self.series.title)
        if show_xlabel:
            axes.set_xlabel(f"Time ({self.series.time_unit})")
        if show_ylabel:
            axes.set_ylabel(f"{self.series.title} ({self.series.unit})")
