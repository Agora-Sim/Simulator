# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import ClassVar
from numpy.typing import NDArray
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ..axis import Axis
from ...instantiation import SimulationSpecs
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Metric(ABC):
    name: ClassVar[str]
    unit: str
    title: ClassVar[str]
    plot_kind: ClassVar[str]

    @abstractmethod
    def calculate(self, state: SimulationState) -> float: ...

    def x_axis(self, specs: SimulationSpecs) -> Axis:

        return Axis(
            values=_compute_timepoints(specs), label="Time", unit=specs.step_size.unit
        )


def _compute_timepoints(simulation_specs: SimulationSpecs) -> NDArray:
    max_duration = simulation_specs.max_duration
    step_type = simulation_specs.step_size

    return np.arange(max_duration + 1) * step_type.factor
