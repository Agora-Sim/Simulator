# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass

from ..node import Node
from .node_blueprint import NodeBlueprint
from .module_property import ModuleProperty
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
    def build_nodes(self, node_blueprint: NodeBlueprint) -> list[Node]:
        nodes = []
        id = 0
        for node_type_name in node_blueprint.type_names:
            new_nodes, next_id = _build_specific_node_type(
                node_blueprint, node_type_name, id
            )

            id = next_id
            nodes.extend(new_nodes)

        return nodes

    def build_connectivity_matrix(
        self, nodes: list[Node], node_blueprint: NodeBlueprint
    ) -> ConnectivityMatrix:
        n = node_blueprint.nr_nodes
        matrix = np.zeros((n, n))

        for node in nodes:
            type = node.node_type
            connectivity = node_blueprint.get_node_type_properties(type).connectivity
            id = node.id

            row = matrix[id]
            matrix[id] = connectivity.build(id, row)

        return ConnectivityMatrix(matrix)


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def _build_specific_node_type(
    node_blueprint: NodeBlueprint, type_name: str, start_id: int
) -> tuple[list[Node], int]:
    node_prop = node_blueprint.get_node_type_properties(type_name)
    nodes = []

    for _ in range(node_prop.initial_numbers):
        module_list = node_prop.modules
        modules = _build_modules(module_list)

        nodes.append(Node(id=start_id, node_type=node_prop.name, modules=modules))
        start_id += 1

    return nodes, start_id


def _build_modules(module_list: list[ModuleProperty]) -> list[NodeModule]:
    modules = []
    for module_type in module_list:
        module = _build_variables(module_type)

        modules.append(module)

    return modules


def _build_variables(module_type: ModuleProperty) -> NodeModule:
    module_class = MODULE_REGISTRY[module_type.name]
    kwargs = {}

    for variable in module_type.variables:
        kwargs[variable] = module_type.sample(variable)

    return module_class(**kwargs)
