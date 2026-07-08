# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .node_property import NodeProperty


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeBlueprint:
    data: dict

    @property
    def type_names(self) -> list[str]:
        return list(self.data.keys())

    @property
    def node_properties(self) -> list[NodeProperty]:
        return [
            NodeProperty(name=name, data=self.data[name]) for name in self.type_names
        ]

    @property
    def nr_nodes(self) -> int:
        total = 0

        for node in self.node_properties:
            total += node.initial_numbers

        return total

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def get_node_type_properties(self, name: str) -> NodeProperty:
        return NodeProperty(name=name, data=self.data[name])
