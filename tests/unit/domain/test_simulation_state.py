"""Contract tests for SimulationState.

SimulationState is a snapshot value object: the nodes, their connectivity and
the time index at which the snapshot was taken.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.simulation_state import SimulationState
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from tests.helpers.builders import build_node


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_simulation_state_stores_its_fields() -> None:
    nodes = [build_node(node_id=0), build_node(node_id=1)]
    connectivity = ConnectivityMatrix(data=np.zeros((2, 2)))

    state = SimulationState(nodes=nodes, connectivity_matrix=connectivity, time_idx=5)

    assert state.nodes == nodes
    assert state.connectivity_matrix is connectivity
    assert state.time_idx == 5


@pytest.mark.unit
def test_simulation_state_accepts_empty_population() -> None:
    connectivity = ConnectivityMatrix(data=np.zeros((0, 0)))

    state = SimulationState(nodes=[], connectivity_matrix=connectivity, time_idx=0)

    assert state.nodes == []
    assert state.time_idx == 0
