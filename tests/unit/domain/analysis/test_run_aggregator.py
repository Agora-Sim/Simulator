"""Contract tests for RunAggregator metadata propagation.

RunAggregator turns per-run histories into one MetricSeries. Beyond the mean/
std maths it must carry the metric's descriptive fields onto the series: name
and title directly, and unit/label onto the y Axis, since downstream rendering
labels each plot from its Axis.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.analysis import RunAggregator
from simulator.domain.analysis.metrics import AgeMetric

from tests.helpers.builders import build_engine, build_simulation


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_aggregate_copies_metric_metadata_onto_series() -> None:
    run = build_simulation(engine=build_engine())
    series = RunAggregator().aggregate([run], AgeMetric(unit="years"))

    assert series.name == "age_metric"
    assert series.title == "Age Metric"
    assert series.y.unit == "years"
    assert series.y.label == "Age Metric"
    assert series.x.label == "Time"
    assert series.plot_kind == "line"


@pytest.mark.unit
def test_aggregate_averages_metric_over_runs() -> None:
    run = build_simulation(engine=build_engine())
    series = RunAggregator().aggregate([run], AgeMetric(unit="years"))

    # The default engine's sole living HealthModule node is aged 25.
    np.testing.assert_array_equal(series.y.values, np.array([25.0]))
    np.testing.assert_array_equal(series.std, np.array([0.0]))
