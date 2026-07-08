# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .module_property import ModuleProperty


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
        connectivity: int
            The average connectivity of nodes of this type. (from 0 - 1)
    """

    name: str
    modules: list[ModuleProperty]
    initial_numbers: int
    connectivity: int
