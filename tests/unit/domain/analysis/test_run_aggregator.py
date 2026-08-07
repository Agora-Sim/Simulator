"""Contract tests for RunAggregator metadata propagation.

RunAggregator turns per-run histories into one BaseAggregator, dispatching
via the metric's `build_result` — MetricSeries for scalar metrics, MetricField
for array-shaped ones. Beyond the mean/std maths it must carry the metric's
descriptive fields onto the result: name and title directly, and unit/label
onto the y Axis, since downstream rendering picks its renderer from
`plot_kind` and reads whichever container shape it gets back.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.analysis import RunAggregator, MetricField
from simulator.domain.analysis.metrics import AgeMetric, AgeDistributionMetric

from tests.helpers.builders import (
    build_engine,
    build_node,
    build_simulation,
    build_health_module,
    build_connectivity_matrix,
)


# ================================================================
# 1. Section: Builders
# ================================================================
def _single_node_run(age: float):
    """A one-run history with a single living HealthModule node of this age."""
    node = build_node(modules=[build_health_module(age=age)])
    engine = build_engine(
        nodes=[node],
        connectivity_matrix=build_connectivity_matrix(data=np.zeros((1, 1))),
    )
    return build_simulation(engine=engine)


# ================================================================
# 2. Section: Unit Tests — scalar metrics -> MetricSeries
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


# ================================================================
# 3. Section: Unit Tests — array-shaped metrics -> MetricField
# ================================================================
@pytest.mark.unit
def test_aggregate_dispatches_array_shaped_metrics_to_a_field() -> None:
    # 4 bins of width 25 over 0..100: age 10 lands in bin 0, age 60 in bin 2.
    metric = AgeDistributionMetric(unit="years", bin_min=0.0, bin_max=100.0, nr_bins=4)
    runs = [_single_node_run(10.0), _single_node_run(60.0)]

    field = RunAggregator().aggregate(runs, metric)

    assert isinstance(field, MetricField)
    assert field.name == "age_distribution_metric"
    assert field.plot_kind == "heatmap"
    # one run lands in bin 0, the other in bin 2 -> both average to 0.5.
    np.testing.assert_array_equal(field.values, np.array([[0.5, 0.0, 0.5, 0.0]]))
