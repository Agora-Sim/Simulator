"""Contract tests for NodeFactory.

NodeFactory turns a NodeBlueprint into a list of Node objects and a
ConnectivityMatrix.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.node import Node
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.instantiation.node_blueprint import NodeBlueprint
from simulator.domain.instantiation.node_factory import (
    NodeFactory,
    MODULE_REGISTRY,
)
from simulator.domain.modules import HealthModule, MoneyModule
from tests.helpers.builders import build_nodes_data


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_module_registry_maps_names_to_classes() -> None:
    assert MODULE_REGISTRY[HealthModule.name] is HealthModule
    assert MODULE_REGISTRY[MoneyModule.name] is MoneyModule


@pytest.mark.unit
def test_build_connectivity_matrix_is_square_over_all_nodes() -> None:
    nodes = [Node(id=0, node_type="citizen", modules=[])]
    blueprint = NodeBlueprint(build_nodes_data())  # 3 citizens + 2 companies

    rng = np.random.default_rng(0)
    matrix = NodeFactory().build_connectivity_matrix(nodes, blueprint, rng)

    assert isinstance(matrix, ConnectivityMatrix)
    assert matrix.data.shape == (blueprint.nr_nodes, blueprint.nr_nodes)


@pytest.mark.unit
def test_build_nodes_creates_one_node_per_initial_number() -> None:
    blueprint = NodeBlueprint(build_nodes_data())  # 3 citizens + 2 companies

    nodes = NodeFactory().build_nodes(blueprint, np.random.default_rng(0))

    assert len(nodes) == 5
    # Sequential ids across all node types.
    assert [node.id for node in nodes] == [0, 1, 2, 3, 4]
    assert [node.node_type for node in nodes] == [
        "citizen",
        "citizen",
        "citizen",
        "company",
        "company",
    ]
