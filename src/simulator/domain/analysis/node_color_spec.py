# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeColorSpec:
    node_type: str
    module_name: str
    variable: str
    colormap: str = "Viridis"
