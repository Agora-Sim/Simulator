# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from dataclasses import dataclass

from .property_range import PropertyRange
from .normal_distribution import NormalDistribution
from .property_distribution import PropertyDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class VariableProperty:
    data: dict[str, Any]

    @property
    def range(self) -> PropertyRange:
        range_list = self.data["range"]
        return PropertyRange.from_list(range_list)

    @property
    def distribution(self) -> PropertyDistribution:
        dist_type = self.data["distribution"]["type"]
        if dist_type == "normal":
            return NormalDistribution(data=self.data["distribution"])

        raise ValueError(f"Unknown distribution type: {dist_type}")

    def sample(self) -> float:
        return self.distribution.sample()
