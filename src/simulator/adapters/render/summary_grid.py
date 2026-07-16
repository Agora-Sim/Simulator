# ================================================================
# 0. Section: IMPORTS
# ================================================================
import math

from matplotlib import pyplot as plt

from dataclasses import dataclass
from matplotlib.figure import Figure

from .metric_plot import MetricPlot
from ...domain.analysis import MetricSeries


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SummaryGrid:
    """Arrange several MetricSeries as a grid of subplots.

    The grid shape adapts to the number of series. When every plot in a column shares
    the same x unit, they are given a common x range so their ticks align and the x
    label and ticks are drawn only on the bottom edge of that column; the same holds
    row-wise for the y axis. Otherwise each plot keeps its own labels and ticks.
    """

    series: list[MetricSeries]
    ncols: int | None = None
    cell_size: tuple[float, float] = (4.0, 3.0)

    def render(self) -> Figure:
        nrows, ncols = self._grid_shape()
        width = ncols * self.cell_size[0]
        height = nrows * self.cell_size[1]
        figure, axes = plt.subplots(
            nrows, ncols, figsize=(width, height), squeeze=False
        )

        shared_x_cols = self._shared_x_columns(nrows, ncols)
        shared_y_rows = self._shared_y_rows(nrows, ncols)

        for index, series in enumerate(self.series):
            row, col = divmod(index, ncols)
            # x edge is the bottom-most filled cell of the column.
            show_x = not shared_x_cols[col] or _is_bottom_of_column(
                index, ncols, len(self.series)
            )
            show_y = not shared_y_rows[row] or col == 0
            _draw_cell(axes[row][col], series, show_x, show_y)

        self._unify_shared_ranges(axes, nrows, ncols, shared_x_cols, shared_y_rows)
        self._hide_empty_cells(axes, nrows, ncols)
        figure.tight_layout()
        return figure

    # ================================================================
    # 2. Section: Methods — layout helpers
    # ================================================================
    def _grid_shape(self) -> tuple[int, int]:
        count = len(self.series)
        ncols = self.ncols or math.ceil(math.sqrt(count))
        ncols = max(1, min(ncols, count))
        nrows = math.ceil(count / ncols)
        return nrows, ncols

    def _shared_x_columns(self, nrows: int, ncols: int) -> list[bool]:
        """True per column when all its plots share the same x unit."""
        shared = []
        for col in range(ncols):
            units = [s.time_unit for s in self._column_series(col, nrows, ncols)]
            shared.append(_all_equal(units))
        return shared

    def _shared_y_rows(self, nrows: int, ncols: int) -> list[bool]:
        """True per row when all its plots share the same y unit."""
        shared = []
        for row in range(nrows):
            units = [s.unit for s in self._row_series(row, ncols)]
            shared.append(_all_equal(units))
        return shared

    def _unify_shared_ranges(
        self, axes, nrows: int, ncols: int, shared_x_cols, shared_y_rows
    ) -> None:
        """Give shared columns/rows a common range so their ticks align."""
        for col in range(ncols):
            if not shared_x_cols[col]:
                continue
            cells = self._column_cells(axes, col, nrows, ncols)
            limits = _union_limits(cell.get_xlim() for cell in cells)
            for cell in cells:
                cell.set_xlim(limits)
        for row in range(nrows):
            if not shared_y_rows[row]:
                continue
            cells = self._row_cells(axes, row, ncols)
            limits = _union_limits(cell.get_ylim() for cell in cells)
            for cell in cells:
                cell.set_ylim(limits)

    def _column_series(self, col: int, nrows: int, ncols: int) -> list[MetricSeries]:
        indices = [row * ncols + col for row in range(nrows)]
        return [self.series[i] for i in indices if i < len(self.series)]

    def _row_series(self, row: int, ncols: int) -> list[MetricSeries]:
        start = row * ncols
        return self.series[start : start + ncols]

    def _column_cells(self, axes, col: int, nrows: int, ncols: int) -> list:
        indices = [row * ncols + col for row in range(nrows)]
        return [axes[i // ncols][col] for i in indices if i < len(self.series)]

    def _row_cells(self, axes, row: int, ncols: int) -> list:
        count = len(self._row_series(row, ncols))
        return [axes[row][col] for col in range(count)]

    def _hide_empty_cells(self, axes, nrows: int, ncols: int) -> None:
        for index in range(len(self.series), nrows * ncols):
            row, col = divmod(index, ncols)
            axes[row][col].axis("off")


# ================================================================
# 3. Section: Functions — cell drawing
# ================================================================
def _draw_cell(axes, series: MetricSeries, show_x: bool, show_y: bool) -> None:
    MetricPlot(series).draw(axes, show_xlabel=show_x, show_ylabel=show_y)
    if not show_x:
        axes.tick_params(labelbottom=False)
    if not show_y:
        axes.tick_params(labelleft=False)


def _union_limits(limits) -> tuple[float, float]:
    """Smallest interval covering every (low, high) pair."""
    lows, highs = zip(*limits)
    return (min(lows), max(highs))


def _all_equal(values: list) -> bool:
    return all(value == values[0] for value in values[1:])


def _is_bottom_of_column(index: int, ncols: int, count: int) -> bool:
    """The plot is the last filled one in its column."""
    return index + ncols >= count
