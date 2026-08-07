# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from numpy.typing import NDArray
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ConnectivityMatrix:
    data: NDArray

    def copy(self) -> "ConnectivityMatrix":
        return ConnectivityMatrix(data=self.data.copy())

    def get_most_connected(self):
        pass
