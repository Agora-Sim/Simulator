# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass, field

from simulator.domain.analysis.axis import Axis

from .metrics import Metric
from .metric_series import MetricSeries
from ..simulation_run import SimulationRun
from .metric_extractor import MetricExtractor


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
        x_axis = metric.x_axis(simulation_specs)

        run_values = []
        for run in runs_histories:
            values = self._extractor.extract(run.history, metric)
            run_values.append(values)

        y_axis = Axis(
            values=np.mean(run_values, axis=0),
            label=metric.title,
            unit=metric.unit,
        )

        std = np.std(run_values, axis=0)

        metric_series = MetricSeries(
            name=metric.name,
            title=metric.title,
            x=x_axis,
            y=y_axis,
            std=std,
            plot_kind=metric.plot_kind,
        )

        return metric_series
