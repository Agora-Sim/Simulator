# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import TypeVar
from dataclasses import dataclass

from .modules import NodeModule

M = TypeVar("M", bound=NodeModule)


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Node:
    id: int
    node_type: str
    modules: list[NodeModule]
    status: bool = True

    def __post_init__(self):
        for module in self.modules:
            module.node_id = self.id

    def has_module(self, module_type: type[NodeModule]) -> bool:
        return any(isinstance(m, module_type) for m in self.modules)

    def get_module(self, module_type: type[M]) -> M | None:
        return next((m for m in self.modules if isinstance(m, module_type)), None)
