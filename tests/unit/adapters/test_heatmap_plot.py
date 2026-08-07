"""Unit tests for HeatmapPlot.

HeatmapPlot draws a MetricField's (steps, bins) values as an image with time
along x. The values are transposed on the way in so rows are bins, and the
extent is widened by half a bin because the field's y coordinates are bin
centres. Matplotlib runs headless (Agg).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from matplotlib import pyplot as plt

from simulator.adapters.render import MetricPlot
from simulator.domain.analysis import Axis, MetricField
from simulator.adapters.render.metric_renders import HeatmapPlot


# ================================================================
# 1. Section: Builders
# ================================================================
def _field() -> MetricField:
    # 3 steps x 4 bins, centres at 12.5..87.5 for bins of width 25 over 0..100.
    return MetricField(
        name="age_distribution_metric",
        title="Age Distribution",
        x=Axis(values=np.arange(3, dtype=float), label="Time", unit="month"),
        y=Axis(values=np.array([12.5, 37.5, 62.5, 87.5]), label="Age", unit="months"),
        values=np.arange(12, dtype=float).reshape(3, 4),
        plot_kind="heatmap",
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_heatmap_kind_resolves_to_heatmap_plot() -> None:
    assert isinstance(MetricPlot(_field()).renderer, HeatmapPlot)
    plt.close("all")


@pytest.mark.unit
def test_draw_puts_bins_on_rows_and_time_on_columns() -> None:
    _, axes = plt.subplots()

    HeatmapPlot(colorbar=False).draw(axes, _field())

    # values are (3 steps, 4 bins); the image must be (4 rows, 3 cols).
    assert axes.images[0].get_array().shape == (4, 3)
    plt.close("all")


@pytest.mark.unit
def test_draw_extends_the_image_by_half_a_bin_past_the_centres() -> None:
    _, axes = plt.subplots()

    HeatmapPlot(colorbar=False).draw(axes, _field())

    assert tuple(axes.images[0].get_extent()) == (0.0, 2.0, 0.0, 100.0)
    plt.close("all")


@pytest.mark.unit
def test_draw_labels_the_axes_from_the_field() -> None:
    _, axes = plt.subplots()

    MetricPlot(_field()).draw(axes)

    assert axes.get_title() == "Age Distribution"
    assert axes.get_xlabel() == "Time (month)"
    assert axes.get_ylabel() == "Age (months)"
    plt.close("all")


@pytest.mark.unit
def test_colorbar_is_attached_when_asked() -> None:
    figure, axes = plt.subplots()

    HeatmapPlot(colorbar=True).draw(axes, _field())

    # the colorbar claims an extra Axes on the figure.
    assert len(figure.axes) == 2
    plt.close("all")


@pytest.mark.unit
def test_a_single_bin_field_still_draws() -> None:
    field = _field()
    field.y = Axis(values=np.array([50.0]), label="Age", unit="months")
    field.values = np.zeros((3, 1))
    _, axes = plt.subplots()

    HeatmapPlot(colorbar=False).draw(axes, field)

    assert tuple(axes.images[0].get_extent()) == (0.0, 2.0, 49.5, 50.5)
    plt.close("all")
