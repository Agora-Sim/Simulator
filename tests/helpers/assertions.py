"""Custom assertions for adapter tests.

Domain dataclasses hold NumPy arrays (ConnectivityMatrix.data), so plain `==`
between two objects raises "ambiguous truth value". These helpers compare the
graph piece by piece, using np.testing for the array leaves, so failures point
at the exact field that diverged after a serialization round-trip.
"""

from __future__ import annotations

import numpy as np

from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.node import Node
from simulator.domain.simulation_engine import SimulationEngine
from simulator.domain.simulation_state import SimulationState
from simulator.domain.simulation_run import SimulationRun


def assert_connectivity_equal(
    actual: ConnectivityMatrix, expected: ConnectivityMatrix
) -> None:
    np.testing.assert_array_equal(actual.data, expected.data)


def assert_nodes_equal(actual: list[Node], expected: list[Node]) -> None:
    # Nodes carry no arrays, so dataclass equality is safe and precise here.
    assert actual == expected


def assert_state_equal(actual: SimulationState, expected: SimulationState) -> None:
    assert actual.time_idx == expected.time_idx
    assert_nodes_equal(actual.nodes, expected.nodes)
    assert_connectivity_equal(actual.connectivity_matrix, expected.connectivity_matrix)


def assert_engine_equal(actual: SimulationEngine, expected: SimulationEngine) -> None:
    assert_nodes_equal(actual.nodes, expected.nodes)
    assert_connectivity_equal(actual.connectivity_matrix, expected.connectivity_matrix)
    assert actual.simulation_specs.data == expected.simulation_specs.data


def assert_simulation_equal(actual: SimulationRun, expected: SimulationRun) -> None:
    assert actual.current_step == expected.current_step
    assert len(actual.history) == len(expected.history)
    for actual_state, expected_state in zip(actual.history, expected.history):
        assert_state_equal(actual_state, expected_state)
    assert_engine_equal(actual.engine, expected.engine)
