# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

from .resource import Resource
from .node_module import NodeModule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ResourcesModule(NodeModule):
    name: ClassVar[str] = "resources_module"

    resources: list[Resource]

    def apply(self):
        pass
