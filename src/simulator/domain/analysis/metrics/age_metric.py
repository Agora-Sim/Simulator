# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

from ...modules import HealthModule, NodeModule
from .module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class AgeMetric(ModuleScalarMetric):
    name: ClassVar[str] = "age_metric"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "age"
    title: ClassVar[str] = "Age Metric"
