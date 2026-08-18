# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import networkx as nx

from dataclasses import dataclass

from ...domain import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NetworkGraphBuilder:
    def build(self, state: SimulationState) -> nx.Graph:
        graph = nx.Graph()
        for node in state.nodes:
            graph.add_node(node.id, node_type=node.node_type, status=node.status)

        # 1. Upper triangle only: the matrix is symmetric, edges are undirected
        matrix = state.connectivity_matrix.data
        rows, cols = np.nonzero(np.triu(matrix, k=1))
        for i, j in zip(rows, cols):
            graph.add_edge(int(i), int(j), weight=float(matrix[i, j]))
        return graph
