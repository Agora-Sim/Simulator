# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib.axes import Axes
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ....domain.analysis import BaseAggregator


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricRenderer[AggregatorT: BaseAggregator](ABC):
    @abstractmethod
    def draw(self, axes: Axes, series: AggregatorT) -> None: ...
