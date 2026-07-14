"""Tests for PercentageConnectivity.

PercentageConnectivity is the rule that makes a node connect to roughly
``percentage`` of the whole population. Two things must hold:

- Locally (the ``build`` method): a node only ever samples *forward* nodes
  (higher ids), measures its target against the *full* population (n - 1), and
  never asks for more connections than there are candidates left.
- Globally (a matrix built from many such nodes): the graph stays undirected
  (symmetric, no self-loops, binary), and in a population made only of these
  nodes the mean connectivity fraction tracks ``percentage`` within ~10%.

The regression tests here were written against a bug where the target
percentage was measured against only the reachable-forward nodes instead of
the whole population, which pulled the mean connectivity well below the target.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.instantiation.connectivity import PercentageConnectivity
from simulator.domain.instantiation.node_blueprint import NodeBlueprint
from simulator.domain.instantiation.node_factory import NodeFactory
from tests.helpers.builders import (
    build_percentage_connectivity_data,
    build_homogeneous_percentage_nodes_data,
)


# ================================================================
# 1. Section: Helpers
# ================================================================
def _make_rule(percentage: float) -> PercentageConnectivity:
    return PercentageConnectivity(
        build_percentage_connectivity_data(percentage=percentage)
    )


def _build_matrix(n: int, percentage: float, rng: np.random.Generator) -> np.ndarray:
    """Build one connectivity matrix for a homogeneous percentage population."""
    blueprint = NodeBlueprint(
        build_homogeneous_percentage_nodes_data(n=n, percentage=percentage)
    )
    factory = NodeFactory()
    nodes = factory.build_nodes(blueprint, rng)
    return factory.build_connectivity_matrix(nodes, blueprint, rng).data


def _mean_connectivity_fraction(matrix: np.ndarray) -> float:
    """Average, over all nodes, of (degree / possible connections)."""
    n = matrix.shape[0]
    return float((matrix.sum(axis=1) / (n - 1)).mean())


# ================================================================
# 2. Section: Unit Tests — the build() rule in isolation
# ================================================================
@pytest.mark.unit
def test_percentage_reads_value_from_data() -> None:
    rule = _make_rule(0.7)

    assert rule.percentage == 0.7


@pytest.mark.unit
def test_build_targets_full_population_for_first_node() -> None:
    # Node 0: 0.5 of the other 4 nodes rounds to 2 connections
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [], "candidates": [1, 2, 3, 4]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=0, connection_dict=connection_dict, rng=rng)

    assert len(result) == 2
    assert set(result).issubset({1, 2, 3, 4})


@pytest.mark.unit
def test_build_only_samples_forward_nodes() -> None:
    # Node 2: earlier nodes 0, 1 are off-limits, only 3, 4 are eligible
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [0], "candidates": [1, 3, 4]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=2, connection_dict=connection_dict, rng=rng)

    assert set(result).issubset({3, 4})
    assert 0 not in result
    assert 1 not in result


@pytest.mark.unit
def test_build_measures_target_against_whole_population_not_just_forward() -> None:
    # Regression: universe is n - 1 = 4, target 2, so 1 extra added
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [0], "candidates": [1, 3, 4]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=2, connection_dict=connection_dict, rng=rng)

    assert len(result) == 1


@pytest.mark.unit
def test_build_returns_empty_when_already_connected_enough() -> None:
    # Three existing connections already exceed the target of 2
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [0, 1, 2], "candidates": [4]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=3, connection_dict=connection_dict, rng=rng)

    assert len(result) == 0


@pytest.mark.unit
def test_build_returns_empty_when_no_forward_candidates() -> None:
    # Last node: everything left is an earlier node, nothing to sample
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [0, 1], "candidates": [2, 3]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=4, connection_dict=connection_dict, rng=rng)

    assert len(result) == 0


@pytest.mark.unit
def test_build_clamps_request_to_available_forward_candidates() -> None:
    # Regression: asks for 3 extra but only node 4 is left, must not raise
    rule = _make_rule(1.0)
    connection_dict = {"already_connected": [0], "candidates": [1, 2, 4]}

    rng = np.random.default_rng(0)
    result = rule.build(node_id=3, connection_dict=connection_dict, rng=rng)

    assert set(result) == {4}


@pytest.mark.unit
def test_build_is_reproducible_under_a_fixed_seed() -> None:
    rule = _make_rule(0.5)
    connection_dict = {"already_connected": [], "candidates": [1, 2, 3, 4, 5, 6]}

    first = rule.build(
        node_id=0, connection_dict=connection_dict, rng=np.random.default_rng(123)
    )
    second = rule.build(
        node_id=0, connection_dict=connection_dict, rng=np.random.default_rng(123)
    )

    np.testing.assert_array_equal(first, second)


# ================================================================
# 3. Section: Matrix-Level Tests — the graph invariants
# ================================================================
@pytest.mark.unit
def test_matrix_stays_symmetric() -> None:
    # Bidirectional: if i connects to j, j connects to i
    matrix = _build_matrix(n=40, percentage=0.5, rng=np.random.default_rng(7))

    np.testing.assert_array_equal(matrix, matrix.T)


@pytest.mark.unit
def test_matrix_has_no_self_connections() -> None:
    matrix = _build_matrix(n=40, percentage=0.5, rng=np.random.default_rng(7))

    np.testing.assert_array_equal(np.diag(matrix), np.zeros(40))


@pytest.mark.unit
def test_matrix_is_binary() -> None:
    matrix = _build_matrix(n=40, percentage=0.5, rng=np.random.default_rng(7))

    assert np.isin(matrix, [0.0, 1.0]).all()


# ================================================================
# 4. Section: Statistical Test — mean connectivity tracks the target
# ================================================================
@pytest.mark.unit
@pytest.mark.parametrize("percentage", [0.2, 0.5, 0.8])
def test_mean_connectivity_stays_within_ten_percent_of_target(
    percentage: float,
) -> None:
    # Not guaranteed per-node, so average many builds and allow a ±10% band
    rng = np.random.default_rng(20240101)
    n = 100
    runs = 30

    fractions = [
        _mean_connectivity_fraction(_build_matrix(n=n, percentage=percentage, rng=rng))
        for _ in range(runs)
    ]
    mean_fraction = float(np.mean(fractions))

    assert percentage * 0.9 <= mean_fraction <= percentage * 1.1
