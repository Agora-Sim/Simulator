# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .modules import NodeModule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Node:
    id: int
    node_type: str
    modules: list[NodeModule]
