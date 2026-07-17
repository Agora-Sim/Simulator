"""Contract tests for Node.

Node holds an id, a node_type label, a list of modules and an alive status.
On construction it stamps its id onto every module so effects the modules
emit can name their owning node.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.node import Node
from simulator.domain.modules import MoneyModule, NodeModule

from tests.helpers.builders import build_health_module


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_node_stores_its_fields() -> None:
    modules: list[NodeModule] = [build_health_module(health=80.0, age=25.0)]

    node = Node(id=7, node_type="citizen", modules=modules, status=True)

    assert node.id == 7
    assert node.node_type == "citizen"
    assert node.modules == modules


@pytest.mark.unit
def test_node_accepts_multiple_modules() -> None:
    health = build_health_module(health=50.0, age=30.0)
    money = MoneyModule(balance=100.0, income=10.0)

    node = Node(id=0, node_type="citizen", modules=[health, money])

    assert node.modules == [health, money]


@pytest.mark.unit
def test_node_accepts_empty_module_list() -> None:
    node = Node(id=0, node_type="citizen", modules=[])

    assert node.modules == []


@pytest.mark.unit
def test_nodes_with_equal_fields_are_equal() -> None:
    modules: list[NodeModule] = [build_health_module(health=50.0, age=30.0)]

    a = Node(id=1, node_type="citizen", modules=modules, status=True)
    b = Node(id=1, node_type="citizen", modules=modules)

    assert a == b


@pytest.mark.unit
def test_node_status_defaults_to_alive() -> None:
    node = Node(id=0, node_type="citizen", modules=[])

    assert node.status is True


@pytest.mark.unit
def test_node_stamps_its_id_on_every_module() -> None:
    health = build_health_module(health=50.0, age=30.0)
    money = MoneyModule(balance=100.0, income=10.0)

    Node(id=9, node_type="citizen", modules=[health, money])

    assert health.node_id == 9
    assert money.node_id == 9


@pytest.mark.unit
def test_nodes_with_different_ids_are_not_equal() -> None:
    modules: list[NodeModule] = [build_health_module(health=50.0, age=30.0)]

    a = Node(id=1, node_type="citizen", modules=modules, status=True)
    b = Node(id=2, node_type="citizen", modules=modules)

    assert a != b
