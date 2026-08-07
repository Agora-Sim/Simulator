# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from abc import ABC, abstractmethod
from typing import Any, ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class PropertyDistribution(ABC):
    type: ClassVar[str]
    data: dict[str, Any]

    @abstractmethod
    def sample(self, rng: np.random.Generator) -> float:
        pass
