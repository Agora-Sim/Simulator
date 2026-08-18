# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

"""Unit tests for NetworkGraphBuilder.

The builder turns a SimulationState into an undirected networkx graph: one
node per Node (carrying node_type/status as attributes) and one edge per
non-zero entry of the connectivity matrix. Only the strict upper triangle is
read, since the matrix is symmetric — reading all of it would add every edge
twice and read the diagonal as self-loops.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest
import networkx as nx

# not re-exported by render/: it is NetworkRenderer's internal collaborator
from simulator.adapters.render.network_graph_builder import NetworkGraphBuilder

from tests.helpers.builders import (
    build_connectivity_matrix,
    build_engine,
    build_health_module,
)
from simulator.domain.node import Node


# ================================================================
# 1. Section: Builders
# ================================================================
def _state(matrix: np.ndarray):
    """A state whose population size matches the given square matrix."""
    nodes = [
        Node(id=i, node_type="citizen", modules=[build_health_module()])
        for i in range(len(matrix))
    ]
    return build_engine(
        nodes=nodes,
        connectivity_matrix=build_connectivity_matrix(matrix),
    ).build_state()


def _chain_matrix() -> np.ndarray:
    """A 3-node chain: 0-1 weighted 0.5, 1-2 weighted 1.0, 0-2 absent."""
    return np.array(
        [
            [0.0, 0.5, 0.0],
            [0.5, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_build_adds_one_graph_node_per_simulation_node() -> None:
    graph = NetworkGraphBuilder().build(_state(_chain_matrix()))

    assert sorted(graph.nodes()) == [0, 1, 2]


@pytest.mark.unit
def test_build_carries_node_type_and_status_as_attributes() -> None:
    state = _state(_chain_matrix())
    state.nodes[1].status = False

    graph = NetworkGraphBuilder().build(state)

    assert graph.nodes[0] == {"node_type": "citizen", "status": True}
    assert graph.nodes[1]["status"] is False


@pytest.mark.unit
def test_build_adds_one_edge_per_nonzero_upper_triangle_entry() -> None:
    graph = NetworkGraphBuilder().build(_state(_chain_matrix()))

    assert sorted(tuple(sorted(e)) for e in graph.edges()) == [(0, 1), (1, 2)]


@pytest.mark.unit
def test_build_stores_the_matrix_entry_as_the_edge_weight() -> None:
    graph = NetworkGraphBuilder().build(_state(_chain_matrix()))

    assert graph.edges[0, 1]["weight"] == 0.5
    assert graph.edges[1, 2]["weight"] == 1.0


@pytest.mark.unit
def test_build_ignores_the_diagonal_so_there_are_no_self_loops() -> None:
    matrix = _chain_matrix()
    matrix[1, 1] = 1.0

    graph = NetworkGraphBuilder().build(_state(matrix))

    assert not list(nx.selfloop_edges(graph))


@pytest.mark.unit
def test_build_keeps_isolated_nodes() -> None:
    matrix = np.zeros((3, 3))

    graph = NetworkGraphBuilder().build(_state(matrix))

    assert sorted(graph.nodes()) == [0, 1, 2]
    assert not list(graph.edges())


@pytest.mark.unit
def test_build_returns_python_scalars_not_numpy_types() -> None:
    graph = NetworkGraphBuilder().build(_state(_chain_matrix()))

    node_id = next(iter(graph.nodes()))
    assert type(node_id) is int
    assert type(graph.edges[0, 1]["weight"]) is float
