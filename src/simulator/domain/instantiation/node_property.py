# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from dataclasses import dataclass

from .module_properties import ModuleProperty
from .connectivity_rule import ConnectivityRule
from .normal_connectivity import NormalConnectivity


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeProperty:
    """Stores the config values spefied by the user for this node type.

    This class stores the node type specs. It is used by
    NodeFactory during Simulation Engine creation.

    Attributes
    ----------
        name: str
            The name of the node type (e.g citizen)
        modules: list[ModuleProperty]
            A list of module properties to be used by this node type.
        initial_numbers: int
            The initial number of nodes of this type (e.g 1000).
        connectivity: ConnectivityRule
            The connectivity rule to be used by this node type.
    """

    name: str
    data: dict[str, Any]

    @property
    def initial_numbers(self) -> int:
        return self.data["initial_numbers"]

    @property
    def connectivity(self) -> ConnectivityRule:
        con_type = self.data["connectivity"]["type"]
        if con_type == "normal":
            return NormalConnectivity(self.data["connectivity"])

        raise ValueError(f"Unknown connectivity type: {con_type}")

    @property
    def modules(self) -> list[ModuleProperty]:
        modules_names = self.data["modules"].keys()

        return [
            ModuleProperty(name=name, data=self.data["modules"][name])
            for name in modules_names
        ]
