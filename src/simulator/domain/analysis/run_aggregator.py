# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from numpy.typing import NDArray
from dataclasses import dataclass, field

from .metrics import Metric
from .metric_series import MetricSeries
from .metric_extractor import MetricExtractor
from ..simulation_run import SimulationRun
from ..instantiation.simulation_specs import SimulationSpecs


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class RunAggregator:
    _extractor: MetricExtractor = field(default_factory=MetricExtractor)

    def aggregate(
        self, runs_histories: list[SimulationRun], metric: Metric
    ) -> MetricSeries:
        simulation_specs = runs_histories[0].engine.simulation_specs
        timepoints = _compute_timepoints(simulation_specs)

        run_values = []
        for run in runs_histories:
            values = self._extractor.extract(run.history, metric)
            run_values.append(values)

        mean = np.mean(run_values, axis=0)
        std = np.std(run_values, axis=0)

        metric_series = MetricSeries(
            name=metric.name,
            title=metric.title,
            unit=metric.unit,
            timepoints=timepoints,
            mean=mean,
            std=std,
            time_unit=simulation_specs.step_size.unit,
        )
        return metric_series


def _compute_timepoints(simulation_specs: SimulationSpecs) -> NDArray:
    max_duration = simulation_specs.max_duration
    step_type = simulation_specs.step_size

    return np.arange(max_duration + 1) * step_type.factor
