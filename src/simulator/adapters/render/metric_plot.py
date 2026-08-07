# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from matplotlib.axes import Axes
from dataclasses import dataclass
from matplotlib.figure import Figure

from .metric_renders import renderer_for
from ...domain.analysis import Axis, BaseAggregator


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricPlot:
    series: BaseAggregator

    @property
    def renderer(self):
        return renderer_for(self.series.plot_kind)

    def render(self) -> Figure:
        figure, axes = plt.subplots()
        self.draw(axes)
        return figure

    def draw(
        self, axes: Axes, show_xlabel: bool = True, show_ylabel: bool = True
    ) -> None:
        self.renderer.draw(axes, self.series)  # type: ignore

        axes.set_title(self.series.title)
        if show_xlabel:
            axes.set_xlabel(_axis_label(self.series.x))
        if show_ylabel:
            axes.set_ylabel(_axis_label(self.series.y))


# ================================================================
# 2. Section: Functions — labelling
# ================================================================
def _axis_label(axis: Axis) -> str:
    return f"{axis.label} ({axis.unit})"
