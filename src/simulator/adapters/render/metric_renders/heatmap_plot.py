# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from matplotlib.axes import Axes

from ....domain.analysis import MetricField
from .metric_renderer import MetricRenderer


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HeatmapPlot(MetricRenderer[MetricField]):
    cmap: str = "viridis"
    colorbar: bool = True

    def draw(self, axes: Axes, series: MetricField) -> None:
        x, y = series.x, series.y
        # values are (steps, bins); imshow wants rows=y, so transpose.
        image = axes.imshow(
            series.values.T,
            origin="lower",
            aspect="auto",
            extent=_extent(x.values, y.values),
            cmap=self.cmap,
        )
        if self.colorbar:
            axes.figure.colorbar(image, ax=axes)


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def _extent(x_values, y_values) -> tuple[float, float, float, float]:
    """Outer edges of the image, from coordinates that are bin centres."""
    half = _half_step(y_values)
    return (
        float(x_values[0]),
        float(x_values[-1]),
        float(y_values[0]) - half,
        float(y_values[-1]) + half,
    )


def _half_step(values) -> float:
    if len(values) < 2:
        return 0.5
    return float(values[1] - values[0]) / 2
