# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any, cast
from dataclasses import dataclass

from .property_range import PropertyRange
from .property_distribution import PropertyDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ModuleProperty:
    name: str
    data: dict[str, Any]

    @property
    def range(self) -> PropertyRange:
        range_list = cast(list, self.data.get("range"))
        return PropertyRange.from_list(range_list)

    @property
    def distribution(self) -> PropertyDistribution:
        data = cast(dict, self.data.get("distribution"))

        return PropertyDistribution(
            name=data["type"],
            data=data["params"],
        )
