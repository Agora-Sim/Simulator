# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass


from .node import Node
from .instantiation.step_type import StepType
from .connectivity_matrix import ConnectivityMatrix


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationState:
    nodes: list[Node]
    connectivity_matrix: ConnectivityMatrix
    time_idx: float
    time_step: StepType
