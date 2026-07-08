# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

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
    def variables(self) -> list[str]:
        return list(self.data.keys())

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def get_range(self, variable: str) -> PropertyRange:
        range_list = cast(dict, self.data[variable]["range"])
        return PropertyRange.from_list(range_list[variable])

    def distribution(self, variable: str) -> PropertyDistribution:
        data = cast(dict, self.data[variable]["distribution"])

        return PropertyDistribution(
            name=data["type"],
            data={key: value for key, value in data.items() if key != "type"},
        )

    def sample(self, variable: str) -> float:
        sampled = self.distribution(variable).sample()
        range = self.get_range(variable)

        return np.clip(sampled, range.min, range.max)
