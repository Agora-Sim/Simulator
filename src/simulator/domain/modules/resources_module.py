# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

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

    def apply(self, rng: np.random.Generator):
        pass
