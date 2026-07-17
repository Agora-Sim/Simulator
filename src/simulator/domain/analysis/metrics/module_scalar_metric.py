# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass
from abc import ABC

from .metric import Metric
from ...modules import NodeModule
from ...simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ModuleScalarMetric(Metric, ABC):
    """Averages one module attribute over every living node carrying it.

    Concrete metrics declare `module` and `attribute` as ClassVars and
    inherit `calculate` unchanged.
    """

    module: ClassVar[type[NodeModule]]
    attribute: ClassVar[str]

    def __post_init__(self) -> None:
        # A. Declared without values here, so an undeclared subclass fails loudly
        if not hasattr(self, "module") or not hasattr(self, "attribute"):
            raise TypeError(
                f"{type(self).__name__} must declare 'module' and 'attribute'"
            )

    def calculate(self, state: SimulationState) -> float:
        values = []
        for node in state.nodes:
            if not node.status:
                continue
            if node.has_module(self.module):
                selected_module = node.get_module(self.module)
                values.append(getattr(selected_module, self.attribute))

        return sum(values) / len(values) if values else 0.0
