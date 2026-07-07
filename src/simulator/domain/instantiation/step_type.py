"""Step type for Simulation Engine creation.

Defines StepType used to define time step specs of the simulation. Should define the
smallest unit value (factor) and the defined unit of time (months, days, years, etc)
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class StepType:
    factor: float
    unit: str

    @classmethod
    def from_str(cls, step_type_str: str) -> "StepType":
        factor, unit = step_type_str.split()
        return cls(factor=float(factor), unit=unit)
