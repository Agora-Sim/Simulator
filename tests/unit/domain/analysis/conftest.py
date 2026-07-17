# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.node import Node
from simulator.domain.simulation_state import SimulationState
from simulator.domain.modules import MoneyModule

from tests.helpers.builders import build_engine, build_health_module


# ================================================================
# 1. Section: Builders
# ================================================================
def _health_node(
    node_id: int,
    age: float = 30.0,
    health: float = 50.0,
    status: bool = True,
) -> Node:
    """A living-by-default node carrying a HealthModule with set values."""
    node = Node(
        id=node_id,
        node_type="citizen",
        modules=[build_health_module(health=health, age=age)],
    )
    node.status = status
    return node


def _money_node(node_id: int) -> Node:
    """A node with no HealthModule, so age/health metrics must skip it."""
    return Node(
        id=node_id,
        node_type="company",
        modules=[MoneyModule(balance=100.0, income=10.0)],
    )


def _state(nodes: list[Node]) -> SimulationState:
    """A frozen SimulationState wrapping the given nodes."""
    return build_engine(nodes=nodes).build_state()


# ================================================================
# 2. Section: Fixtures
# ================================================================
@pytest.fixture
def health_node():
    return _health_node


@pytest.fixture
def money_node():
    return _money_node


@pytest.fixture
def state_of():
    return _state
