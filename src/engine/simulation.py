# ================================================================
# 0. Section: Imports
# ================================================================
import numpy as np
from copy import deepcopy

from ..components import Citizen
from .utils import initiate_connectivity_matrix
from .engine_pieces import Properties, Run


class Simulation(Properties, Run):
    # ================================================================
    # 1. Section: Initializers
    # ================================================================
    def __init__(self, citizens: np.ndarray, connectivity_matrix: np.ndarray):
        self.citizens = citizens
        self.connectivity_matrix = connectivity_matrix

        self.nr_of_citizens = len(citizens)
        self.iterations = 0
        self.citizens_history = [deepcopy(self.citizens)]

    @classmethod
    def random(cls, nr_of_citizens: int) -> "Simulation":
        citizens = np.array([Citizen.random(citizen_id=i) for i in range(nr_of_citizens)])
        connectivity = initiate_connectivity_matrix(nr_of_citizens)
        return cls(citizens, connectivity)