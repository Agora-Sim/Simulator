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

    def build(
        self,
        node_id: int,
        connection_dict: dict[str, list],
        rng: np.random.Generator,
    ) -> NDArray:
        # 1. Extract the data from the connection_dict
        candidates = np.asarray(connection_dict["candidates"])
        current_connections = np.asarray(connection_dict["already_connected"])

        # 2. Universe is every other node (n - 1), not just forward ones
        total_possible_connections = len(current_connections) + len(candidates)

        # 3. Only forward nodes are eligible; earlier ones had their turn
        already_checked_nodes = np.arange(node_id)
        forward_candidates = candidates[~np.isin(candidates, already_checked_nodes)]

        # 4. Round (not truncate) so the mean degree stays on target
        target_nr_connections = int(round(self.percentage * total_possible_connections))
        nr_extra_connections = target_nr_connections - len(current_connections)

        # 5. Skip if already connected enough or nothing left to reach
        if nr_extra_connections <= 0 or len(forward_candidates) == 0:
            return np.asarray([])

        # 6. Never ask for more than the candidates available
        nr_extra_connections = min(nr_extra_connections, len(forward_candidates))

        # 7. Sample the extra forward connections at random
        sampled_candidates = rng.choice(
            forward_candidates, nr_extra_connections, replace=False
        )

        return sampled_candidates
