"""Unit tests for AgeDistributionMetric.

Where AgeMetric averages age over survivors, this bins it: `calculate`
returns one count per bin for the living nodes only, and `build_result` wraps
the run-averaged counts as a MetricField rather than a MetricSeries.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.node import Node
from simulator.domain.analysis import Axis, MetricField
from simulator.domain.modules import HealthModule
from simulator.domain.instantiation.step_type import StepType
from simulator.domain.simulation_state import SimulationState
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.analysis.metrics import AgeDistributionMetric


# ================================================================
# 1. Section: Builders
# ================================================================
def _node(node_id: int, age: float, status: bool = True) -> Node:
    module = HealthModule(
        health=100.0,
        age=age,
        baseline_hazard=8.0e-6,
        rate_of_aging=0.008,
        ind_background_hazard=6.0e-5,
        max_age=1200.0,
    )
    return Node(id=node_id, node_type="citizen", modules=[module], status=status)


def _state(nodes: list[Node]) -> SimulationState:
    return SimulationState(
        nodes=nodes,
        connectivity_matrix=ConnectivityMatrix(data=np.zeros((len(nodes), len(nodes)))),
        time_idx=0,
        time_step=StepType(factor=1.0, unit="month"),
    )


def _metric() -> AgeDistributionMetric:
    # 4 bins of width 25 over 0..100 keeps the arithmetic checkable by hand.
    return AgeDistributionMetric(unit="months", bin_min=0.0, bin_max=100.0, nr_bins=4)


# ================================================================
# 2. Section: Unit Tests — identity
# ================================================================
@pytest.mark.unit
def test_declares_a_heatmap_plot_kind() -> None:
    assert AgeDistributionMetric.plot_kind == "heatmap"
    assert AgeDistributionMetric.name == "age_distribution_metric"
    assert AgeDistributionMetric.attribute == "age"


# ================================================================
# 3. Section: Unit Tests — calculate
# ================================================================
@pytest.mark.unit
def test_calculate_counts_nodes_per_bin() -> None:
    state = _state([_node(0, 10.0), _node(1, 20.0), _node(2, 60.0)])

    counts = _metric().calculate(state)

    # ages 10 and 20 land in bin 0..25; age 60 in bin 50..75.
    assert list(counts) == [2.0, 0.0, 1.0, 0.0]


@pytest.mark.unit
def test_calculate_ignores_dead_nodes() -> None:
    state = _state([_node(0, 10.0), _node(1, 10.0, status=False)])

    counts = _metric().calculate(state)

    assert list(counts) == [1.0, 0.0, 0.0, 0.0]


@pytest.mark.unit
def test_calculate_returns_one_value_per_bin() -> None:
    metric = AgeDistributionMetric(unit="months", nr_bins=7)

    counts = metric.calculate(_state([_node(0, 10.0)]))

    assert counts.shape == (7,)


@pytest.mark.unit
def test_calculate_drops_values_outside_the_bin_range() -> None:
    state = _state([_node(0, 10.0), _node(1, 500.0)])

    counts = _metric().calculate(state)

    assert counts.sum() == 1.0


@pytest.mark.unit
def test_calculate_on_an_empty_population_is_all_zeros() -> None:
    counts = _metric().calculate(_state([]))

    assert list(counts) == [0.0, 0.0, 0.0, 0.0]


# ================================================================
# 4. Section: Unit Tests — build_result
# ================================================================
@pytest.mark.unit
def test_build_result_makes_a_field_with_bin_centres_on_y() -> None:
    metric = _metric()
    x_axis = Axis(values=np.arange(3, dtype=float), label="Time", unit="month")
    mean = np.zeros((3, 4))

    field = metric.build_result(x_axis, mean, np.zeros((3, 4)))

    assert isinstance(field, MetricField)
    assert field.plot_kind == "heatmap"
    assert list(field.y.values) == [12.5, 37.5, 62.5, 87.5]
    assert field.y.unit == "months"
    assert field.values.shape == (3, 4)


# ================================================================
# 5. Section: Unit Tests — validation
# ================================================================
@pytest.mark.unit
def test_rejects_a_non_positive_bin_count() -> None:
    with pytest.raises(ValueError, match="nr_bins"):
        AgeDistributionMetric(unit="months", nr_bins=0)


@pytest.mark.unit
def test_rejects_an_inverted_bin_range() -> None:
    with pytest.raises(ValueError, match="bin_max"):
        AgeDistributionMetric(unit="months", bin_min=100.0, bin_max=0.0)
