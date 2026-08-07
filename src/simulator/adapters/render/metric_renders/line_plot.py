# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from matplotlib.axes import Axes

from .metric_renderer import MetricRenderer
from ....domain.analysis import MetricSeries


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class LinePlot(MetricRenderer[MetricSeries]):
    def draw(self, axes: Axes, series: MetricSeries) -> None:
        x, y = series.x, series.y
        axes.plot(x.values, y.values)
        axes.fill_between(
            x.values,
            y.values - series.std,
            y.values + series.std,
            alpha=0.2,
        )
