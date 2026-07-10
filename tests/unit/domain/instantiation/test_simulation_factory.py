"""Contract tests for SimulationFactory.

SimulationFactory turns a SimulationBlueprint into a runnable Simulation,
delegating node/connectivity construction to a NodeFactory. We inject a fake
NodeFactory so the wiring contract can be tested independently of the (currently
broken) real node-building logic.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.service.simulation_run import SimulationRun
from simulator.domain.node import Node
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.instantiation.simulation_specs import SimulationSpecs
from simulator.domain.instantiation.node_blueprint import NodeBlueprint
from simulator.domain.instantiation.simulation_factory import SimulationFactory
from simulator.domain.instantiation.simulation_blueprint import SimulationBlueprint
from tests.helpers.builders import build_blueprint_data


# ================================================================
# 1. Section: Fixtures
# ================================================================
class FakeNodeFactory:
    """Records the inputs it receives and returns canned nodes/connectivity."""

    def __init__(self) -> None:
        self.nodes = [Node(id=0, node_type="citizen", modules=[])]
        self.matrix = ConnectivityMatrix(data=np.zeros((1, 1)))
        self.build_nodes_arg = None
        self.build_connectivity_args = None

    def build_nodes(self, node_blueprint):
        self.build_nodes_arg = node_blueprint
        return self.nodes

    def build_connectivity_matrix(self, nodes, node_blueprint):
        self.build_connectivity_args = (nodes, node_blueprint)
        return self.matrix


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_build_simulation_returns_simulation_wired_with_engine() -> None:
    fake_factory = FakeNodeFactory()
    factory = SimulationFactory(_node_factory=fake_factory)
    blueprint = SimulationBlueprint(build_blueprint_data())

    simulation = factory.build_simulation(blueprint)

    assert isinstance(simulation, SimulationRun)
    assert simulation.engine.nodes is fake_factory.nodes
    assert simulation.engine.connectivity_matrix is fake_factory.matrix
    assert isinstance(simulation.engine.simulation_specs, SimulationSpecs)
    assert simulation.engine.simulation_specs.max_duration == 10


@pytest.mark.unit
def test_build_simulation_passes_node_blueprint_to_factory() -> None:
    fake_factory = FakeNodeFactory()
    factory = SimulationFactory(_node_factory=fake_factory)
    blueprint = SimulationBlueprint(build_blueprint_data())

    factory.build_simulation(blueprint)

    assert isinstance(fake_factory.build_nodes_arg, NodeBlueprint)
    passed_nodes, passed_blueprint = fake_factory.build_connectivity_args
    assert passed_nodes is fake_factory.nodes
    assert isinstance(passed_blueprint, NodeBlueprint)


@pytest.mark.unit
def test_default_node_factory_is_used_when_none_provided() -> None:
    from simulator.domain.instantiation.node_factory import NodeFactory

    factory = SimulationFactory()

    assert isinstance(factory._node_factory, NodeFactory)
