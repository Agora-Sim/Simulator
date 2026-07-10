"""Contract tests for SimulationEngine.

SimulationEngine holds the mutable simulation entities (nodes, connectivity,
specs). Its step() logic is not implemented yet, so it is intentionally left
untested until real behaviour lands; the only contract we pin today is
construction.
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
# 1. Section: Unit Tests
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
