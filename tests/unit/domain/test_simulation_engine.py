"""Contract tests for SimulationEngine.

SimulationEngine holds the mutable simulation entities (nodes, connectivity,
specs). Its step() logic is not implemented yet, so the contract we can pin
today is construction and the explicit NotImplementedError from step().
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.simulation_engine import SimulationEngine
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.instantiation.simulation_specs import SimulationSpecs
from tests.helpers.builders import build_node, build_simulation_data


# ================================================================
# 1. Section: Fixtures
# ================================================================
def _make_engine() -> SimulationEngine:
    return SimulationEngine(
        nodes=[build_node(node_id=0)],
        connectivity_matrix=ConnectivityMatrix(data=np.zeros((1, 1))),
        simulation_specs=SimulationSpecs(build_simulation_data()),
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_simulation_engine_stores_its_fields() -> None:
    nodes = [build_node(node_id=0)]
    connectivity = ConnectivityMatrix(data=np.zeros((1, 1)))
    specs = SimulationSpecs(build_simulation_data())

    engine = SimulationEngine(
        nodes=nodes,
        connectivity_matrix=connectivity,
        simulation_specs=specs,
    )

    assert engine.nodes == nodes
    assert engine.connectivity_matrix is connectivity
    assert engine.simulation_specs is specs


@pytest.mark.unit
def test_step_raises_not_implemented() -> None:
    engine = _make_engine()

    with pytest.raises(NotImplementedError, match="step is not implemented"):
        engine.step()
