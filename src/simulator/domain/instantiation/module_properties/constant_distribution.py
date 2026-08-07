# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import ClassVar
from dataclasses import dataclass
from .property_distribution import PropertyDistribution


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ConstantDistribution(PropertyDistribution):
    name: ClassVar[str] = "constant"

    @property
    def value(self) -> float:
        return self.data["value"]

    def sample(self, rng: np.random.Generator) -> float:
        return self.value
