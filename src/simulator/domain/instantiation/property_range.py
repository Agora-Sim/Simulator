# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass(frozen=True, slots=True)
class PropertyRange:
    min: float
    max: float

    @classmethod
    def from_list(cls, values: list[float]) -> "PropertyRange":
        return cls(min=values[0], max=values[1])

    def __post_init__(self) -> None:
        if self.min > self.max:
            raise ValueError("Range min cannot be greater than max")
