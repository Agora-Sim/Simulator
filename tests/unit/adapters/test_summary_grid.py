"""Unit tests for SummaryGrid layout and shared-axis logic.

SummaryGrid lays out several MetricSeries as a grid of subplots. The behaviour
under test: the grid shape adapts to the number of series, and when every plot
in a column shares the same x unit/range (or every plot in a row shares the
same y unit/range) the labels and ticks are drawn only on the grid edge.
Matplotlib runs headless (Agg) so these stay filesystem free.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from simulator.domain.analysis import Axis, MetricSeries
from simulator.adapters.render import SummaryGrid


# ================================================================
# 1. Section: Builders
# ================================================================
def _series(
    name: str,
    unit: str = "u",
    scale: float = 1.0,
    time_unit: str = "days",
    length: int = 5,
) -> MetricSeries:
    timepoints = np.arange(length, dtype=float)
    return MetricSeries(
        name=name,
        title=name.title(),
        x=Axis(values=timepoints, label="Time", unit=time_unit),
        y=Axis(values=timepoints * scale, label=name.title(), unit=unit),
        std=np.zeros(length),
        plot_kind="line",
    )


def _axes_of(figure):
    return figure.axes


# ================================================================
# 2. Section: Tests — grid shape
# ================================================================
@pytest.mark.unit
def test_single_series_makes_one_cell() -> None:
    figure = SummaryGrid([_series("a")]).render()

    assert len(_axes_of(figure)) == 1


@pytest.mark.unit
def test_grid_shape_is_square_by_default() -> None:
    # 4 series -> 2x2, so 4 populated axes.
    grid = SummaryGrid([_series(f"m{i}") for i in range(4)])

    nrows, ncols = grid._grid_shape()

    assert (nrows, ncols) == (2, 2)


@pytest.mark.unit
def test_explicit_ncols_is_respected() -> None:
    grid = SummaryGrid([_series(f"m{i}") for i in range(3)], ncols=1)

    nrows, ncols = grid._grid_shape()

    assert (nrows, ncols) == (3, 1)


@pytest.mark.unit
def test_empty_trailing_cells_are_turned_off() -> None:
    # 3 series in a 2x2 grid -> one leftover cell is hidden (axis off).
    figure = SummaryGrid([_series(f"m{i}") for i in range(3)]).render()

    off = [ax for ax in figure.axes if not ax.axison]
    assert len(off) == 1


# ================================================================
# 3. Section: Tests — shared x axis (columns)
# ================================================================
@pytest.mark.unit
def test_shared_x_column_labels_only_bottom_edge() -> None:
    # Two series stacked in one column share x unit.
    grid = SummaryGrid([_series("top"), _series("bottom")], ncols=1)
    figure = grid.render()

    top, bottom = figure.axes
    assert top.get_xlabel() == ""
    assert bottom.get_xlabel() != ""


@pytest.mark.unit
def test_different_x_unit_keeps_labels_on_every_plot() -> None:
    top = _series("top")
    bottom = _series("bottom", time_unit="years")
    figure = SummaryGrid([top, bottom], ncols=1).render()

    top_ax, bottom_ax = figure.axes
    assert top_ax.get_xlabel() != ""
    assert bottom_ax.get_xlabel() != ""


@pytest.mark.unit
def test_same_x_unit_different_range_gets_unified_xlim() -> None:
    # Same time unit but different lengths -> both share the wider x range.
    short = _series("top")
    longer = _series("bottom", length=9)
    figure = SummaryGrid([short, longer], ncols=1).render()

    top_ax, bottom_ax = figure.axes
    assert top_ax.get_xlim() == bottom_ax.get_xlim()


# ================================================================
# 4. Section: Tests — shared y axis (rows)
# ================================================================
@pytest.mark.unit
def test_shared_y_row_labels_only_left_edge() -> None:
    # Two series side by side in one row share y unit and range.
    grid = SummaryGrid([_series("left"), _series("right")], ncols=2)
    figure = grid.render()

    left, right = figure.axes
    assert left.get_ylabel() != ""
    assert right.get_ylabel() == ""


@pytest.mark.unit
def test_different_y_unit_keeps_labels_on_every_plot() -> None:
    left = _series("left", unit="kg")
    right = _series("right", unit="m")
    figure = SummaryGrid([left, right], ncols=2).render()

    left_ax, right_ax = figure.axes
    assert left_ax.get_ylabel() != ""
    assert right_ax.get_ylabel() != ""


@pytest.mark.unit
def test_same_y_unit_different_range_gets_unified_ylim() -> None:
    # age and health share a unit but span different ranges -> unified y range.
    age = _series("age", unit="score", scale=10.0)
    health = _series("health", unit="score", scale=1.0)
    figure = SummaryGrid([age, health], ncols=2).render()

    left_ax, right_ax = figure.axes
    assert left_ax.get_ylim() == right_ax.get_ylim()
    assert right_ax.get_ylabel() == ""
