"""Unit tests for renderer selection.

MetricPlot delegates the marks to a MetricRenderer resolved from the series'
`plot_kind` via the registry on every access — it cannot be overridden.
Matplotlib runs headless (Agg).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from dataclasses import dataclass
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from simulator.domain.analysis import Axis, MetricSeries
from simulator.adapters.render import MetricPlot
from simulator.adapters.render import metric_plot as metric_plot_module
from simulator.adapters.render.metric_renders import (
    LinePlot,
    MetricRenderer,
    renderer_for,
)


# ================================================================
# 1. Section: Builders
# ================================================================
def _series(plot_kind: str = "line") -> MetricSeries:
    timepoints = np.arange(5, dtype=float)
    return MetricSeries(
        name="age_metric",
        title="Age Metric",
        x=Axis(values=timepoints, label="Time", unit="days"),
        y=Axis(values=timepoints, label="Age Metric", unit="years"),
        std=np.zeros(5),
        plot_kind=plot_kind,
    )


@dataclass
class _SpyRenderer(MetricRenderer):
    """Records the (axes, series) pairs it was asked to draw."""

    drawn: list = None

    def __post_init__(self) -> None:
        self.drawn = []

    def draw(self, axes: Axes, series: MetricSeries) -> None:
        self.drawn.append((axes, series))


# ================================================================
# 2. Section: Unit Tests — registry
# ================================================================
@pytest.mark.unit
def test_line_kind_resolves_to_line_plot() -> None:
    assert isinstance(renderer_for("line"), LinePlot)


@pytest.mark.unit
def test_unknown_kind_raises_with_the_known_kinds() -> None:
    with pytest.raises(KeyError, match="line"):
        renderer_for("bar")


# ================================================================
# 3. Section: Unit Tests — MetricPlot wiring
# ================================================================
@pytest.mark.unit
def test_renderer_defaults_to_the_one_for_the_series_plot_kind() -> None:
    assert isinstance(MetricPlot(_series()).renderer, LinePlot)


@pytest.mark.unit
def test_draw_delegates_the_series_to_the_resolved_renderer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # patches the registry lookup itself, since renderer can't be injected.
    spy = _SpyRenderer()
    monkeypatch.setattr(metric_plot_module, "renderer_for", lambda plot_kind: spy)
    _, axes = plt.subplots()
    series = _series()

    MetricPlot(series).draw(axes)

    assert spy.drawn == [(axes, series)]
    plt.close("all")


@pytest.mark.unit
def test_line_plot_draws_a_line_and_a_std_band() -> None:
    _, axes = plt.subplots()

    LinePlot().draw(axes, _series())

    assert len(axes.get_lines()) == 1
    assert len(axes.collections) == 1
    plt.close("all")
