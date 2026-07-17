"""Unit tests for MetricPlot labelling.

MetricPlot draws one MetricSeries onto an Axes. The axes title is the series'
human-readable `title` (not its machine `name`), while each axis label is
built from that Axis' own label and unit as "label (unit)". Matplotlib runs
headless (Agg).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from matplotlib import pyplot as plt

from simulator.domain.analysis import Axis, MetricSeries
from simulator.adapters.render import MetricPlot


# ================================================================
# 1. Section: Builders
# ================================================================
def _series() -> MetricSeries:
    timepoints = np.arange(5, dtype=float)
    return MetricSeries(
        name="age_metric",
        title="Age Metric",
        x=Axis(values=timepoints, label="Time", unit="days"),
        y=Axis(values=timepoints, label="Age Metric", unit="years"),
        std=np.zeros(5),
        plot_kind="line",
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_draw_titles_the_axes_with_the_series_title() -> None:
    _, axes = plt.subplots()

    MetricPlot(_series()).draw(axes)

    assert axes.get_title() == "Age Metric"
    plt.close("all")


@pytest.mark.unit
def test_draw_labels_axes_from_title_not_name() -> None:
    _, axes = plt.subplots()

    MetricPlot(_series()).draw(axes)

    assert axes.get_xlabel() == "Time (days)"
    assert axes.get_ylabel() == "Age Metric (years)"
    plt.close("all")
