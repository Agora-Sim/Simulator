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

    # ================================================================
    # 2. Section: FUNCTIONS
    # ================================================================
    def get_node_type_properties(self, name: str) -> NodeProperty:
        # 1. Get only the dict relative to the holder
        node_dict = _get_node_type_dict(self.data, name)

        # 2. Build the NodeProperty
        return _build_node_property(node_dict, name)


# ──────────────────────────────────────────────────────
# 2.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def _get_node_type_dict(data: dict, name: str) -> dict:
    if name not in data.keys():
        raise ValueError(f"Node type '{name}' not found in data")
    return data[name]


def _build_node_property(node_data: dict, name: str) -> NodeProperty:
    if "modules" not in node_data.keys():
        raise ValueError(f"Node type '{name}' does not have a 'modules' key")
    if "initial_numbers" not in node_data.keys():
        raise ValueError(f"Node type '{name}' does not have an 'initial_numbers' key")
    if "connectivity" not in node_data.keys():
        raise ValueError(f"Node type '{name}' does not have a 'connectivity' key")

    return NodeProperty(
        name=name,
        modules=node_data["modules"],
        initial_numbers=node_data["initial_numbers"],
        connectivity=node_data["connectivity"],
    )
