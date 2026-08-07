# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from numpy.typing import NDArray
from dataclasses import dataclass

from .base_aggregator import BaseAggregator


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricSeries(BaseAggregator):
    std: NDArray
