# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

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
class HealthMetric(ModuleScalarMetric):
    name: ClassVar[str] = "health_metric"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "health"
    unit: str = "%"
    title: ClassVar[str] = "Health Metric"
    plot_kind: ClassVar[str] = "line"
