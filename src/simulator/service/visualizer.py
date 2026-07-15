# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass, field

from ..adapters import Source, SimulationIO
from ..domain.analysis import RunAggregator
from ..domain.analysis.metrics import Metric


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

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def render_metrics(self, metrics: list[Metric], formats: list[str]) -> list[Path]:
        runs = self._io.load_all_runs()

        for metric in metrics:
            series = self._aggregator.aggregate(runs_histories=runs, metric=metric)
