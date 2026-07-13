
# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import ClassVar
from numpy.typing import NDArray
from dataclasses import dataclass

from .connectivity_rule import ConnectivityRule


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class PercentageConnectivity(ConnectivityRule):
    type: ClassVar[str] = "percentage"

    @property
    def percentage(self) -> float:
        return self.data["percentage"]

    def build(self, node_id: int, connection_dict: dict[str, list]) -> NDArray:
        # 1. Extract the data from the connection_dict
        candidates = np.asarray(connection_dict["candidates"])
        current_connections = np.asarray(connection_dict["already_connected"])
        already_checked_nodes = np.arange(node_id)
        candidates = candidates[~np.isin(candidates, already_checked_nodes)]

        total_possible_connections = len(current_connections) + len(candidates)

        # 2. Calculate the target number of connections and extra connections
        target_nr_connections = int(self.percentage * total_possible_connections)
        nr_extra_connections = target_nr_connections - len(current_connections)

        # 3. Ignore if already very connected
        if nr_extra_connections <= 0:
            return np.asarray([])

        # 4. Sample nr_extra_connections random candidates
        sampled_candidates = np.random.choice(candidates, nr_extra_connections, replace=False)

        return sampled_candidates
