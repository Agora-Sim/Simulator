# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from numpy.typing import NDArray
from dataclasses import dataclass

from ..node import Node
from .node_blueprint import NodeBlueprint
from .module_properties import ModuleProperty
from ..connectivity_matrix import ConnectivityMatrix
from ..modules import NodeModule, HealthModule, MoneyModule

# ================================================================
# 1. Section: Registry
# ================================================================
MODULE_REGISTRY: dict[str, type[NodeModule]] = {
    HealthModule.name: HealthModule,
    MoneyModule.name: MoneyModule,
}


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeFactory:
    def build_nodes(
        self, node_blueprint: NodeBlueprint, rng: np.random.Generator
    ) -> list[Node]:
        nodes = []
        node_id = 0
        for node_type_name in node_blueprint.type_names:
            new_nodes, next_id = _build_specific_node_type(
                node_blueprint, node_type_name, node_id, rng
            )

            node_id = next_id
            nodes.extend(new_nodes)

        return nodes

    def build_connectivity_matrix(
        self,
        nodes: list[Node],
        node_blueprint: NodeBlueprint,
        rng: np.random.Generator,
    ) -> ConnectivityMatrix:
        n = node_blueprint.nr_nodes
        matrix = np.zeros((n, n))

        for node in nodes:
            node_type = node.node_type
            connectivity = node_blueprint.get_node_type_properties(
                node_type
            ).connectivity
            node_id = node.id

            connection_dict = _build_conection_dict(node_id, matrix)
            to_connect = connectivity.build(node_id, connection_dict, rng)
            matrix = _update_matrix(matrix, node_id, to_connect)

        return ConnectivityMatrix(matrix)


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def _build_specific_node_type(
    node_blueprint: NodeBlueprint,
    type_name: str,
    start_id: int,
    rng: np.random.Generator,
) -> tuple[list[Node], int]:
    node_prop = node_blueprint.get_node_type_properties(type_name)
    nodes = []

    for _ in range(node_prop.initial_numbers):
        module_list = node_prop.modules
        modules = _build_modules(module_list, rng)

        nodes.append(Node(id=start_id, node_type=node_prop.name, modules=modules))
        start_id += 1

    return nodes, start_id


def _build_modules(
    module_list: list[ModuleProperty], rng: np.random.Generator
) -> list[NodeModule]:
    modules = []
    for module_type in module_list:
        module = _build_variables(module_type, rng)

        modules.append(module)

    return modules


def _build_variables(
    module_type: ModuleProperty, rng: np.random.Generator
) -> NodeModule:
    module_class = MODULE_REGISTRY[module_type.name]
    kwargs = {}

    for variable in module_type.variables:
        variable_prop = module_type.variables[variable]
        kwargs[variable] = variable_prop.sample(rng)

    return module_class(**kwargs)


def _build_conection_dict(node_id: int, matrix: NDArray) -> dict[str, list]:
    row = matrix[node_id]

    already_connected = np.argwhere(row != 0).flatten()
    candidates = np.argwhere(row == 0).flatten()
    candidates = candidates[candidates != node_id]

    return {
        "already_connected": already_connected.tolist(),
        "candidates": candidates.tolist(),
    }


def _update_matrix(matrix: NDArray, node_id: int, to_connect: NDArray) -> NDArray:
    if len(to_connect) == 0:
        return matrix

    matrix[node_id, to_connect] = 1
    matrix[to_connect, node_id] = 1
    return matrix
