# ================================================================
# 0. Section: IMPORTS
# ================================================================
from abc import ABC
from typing import ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ResourceProperty(ABC):
    name: ClassVar[str]

    def apply(self):
        raise NotImplementedError("apply method must be implemented")
