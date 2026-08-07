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
class NormalDistribution(PropertyDistribution):
    name: ClassVar[str] = "normal"

    @property
    def mean(self) -> float:
        return self.data["mean"]

    @property
    def std(self) -> float:
        return self.data["std"]

    def sample(self, rng: np.random.Generator) -> float:
        return rng.normal(self.mean, self.std)
