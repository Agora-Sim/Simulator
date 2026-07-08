# ================================================================
# 0. Section: IMPORTS
# ================================================================
from abc import ABC, abstractmethod
from typing import ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeModule(ABC):
    name: ClassVar[str]

    @abstractmethod
    def apply(self):
        pass
