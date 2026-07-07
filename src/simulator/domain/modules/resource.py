# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .resource_property import ResourceProperty


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Resource:
    name: str
    sell_value: float
    target_value: float
    consume_rate: float
    production_rate: float
    properties: list[ResourceProperty]
