# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass, field

from .metrics import Metric
from ..simulation_run import SimulationRun
from .base_aggregator import BaseAggregator
from .metric_extractor import MetricExtractor


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class RunAggregator:
    _extractor: MetricExtractor = field(default_factory=MetricExtractor)

    def aggregate(
        self, runs_histories: list[SimulationRun], metric: Metric
    ) -> BaseAggregator:
        simulation_specs = runs_histories[0].engine.simulation_specs
        x_axis = metric.x_axis(simulation_specs)

        run_values = []
        for run in runs_histories:
            values = self._extractor.extract(run.history, metric)
            run_values.append(values)

        mean = np.mean(run_values, axis=0)
        std = np.std(run_values, axis=0)

        return metric.build_result(x_axis, mean, std)
