# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass, field

from ..adapters import Source, SimulationIO
from ..domain.analysis import RunAggregator
from ..domain.analysis.metrics import Metric
from ..adapters.render import MetricPlot, SummaryGrid, FigureExporter


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Visualizer:
    simulation_name: str
    simulation_description: str
    base_folder: Path = Path("data")

    _aggregator: RunAggregator = field(default_factory=RunAggregator)

    @property
    def _source(self) -> Source:
        return Source(
            simulation_name=self.simulation_name,
            simulation_description=self.simulation_description,
            base_folder=self.base_folder,
        )

    @property
    def _io(self) -> SimulationIO:
        return SimulationIO(self._source)

    @property
    def _figure_exporter(self):
        return FigureExporter(self._source)

    def __post_init__(self):
        self._io.init_figures()

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def render_metrics(self, metrics: list[Metric], formats: list[str]) -> list[Path]:
        runs = self._io.load_all_runs()

        paths = []
        for metric in metrics:
            series = self._aggregator.aggregate(runs_histories=runs, metric=metric)
            figure = MetricPlot(series).render()
            path_list = self._figure_exporter.export(figure, series.name, formats)
            paths.extend(path_list)

        return paths

    def render_summary_grid(
        self,
        metrics: list[Metric],
        formats: list[str],
        name: str = "summary",
        ncols: int | None = None,
    ) -> list[Path]:
        runs = self._io.load_all_runs()

        series = [
            self._aggregator.aggregate(runs_histories=runs, metric=metric)
            for metric in metrics
        ]
        figure = SummaryGrid(series, ncols=ncols).render()
        return self._figure_exporter.export(figure, name, formats)
