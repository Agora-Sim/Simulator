# ================================================================
# 0. Section: Imports
# ================================================================
import pickle

import numpy as np
from copy import deepcopy

from ..logger import logger
from ..components import Citizen
from .utils import initiate_connectivity_matrix
from .engine_pieces import Properties, Run
from ..time import iterations_to_simtime


class Simulation(Properties, Run):
    # ================================================================
    # 1. Section: Initializers
    # ================================================================
    def __init__(self, citizens: np.ndarray, connectivity_matrix: np.ndarray):
        self.citizens = citizens
        self.connectivity_matrix = connectivity_matrix

        self.iterations = 0

        self.citizens_history = [deepcopy(self.citizens)]
        self.connectivity_matrix_history = [deepcopy(self.connectivity_matrix)]

    @classmethod
    def random(cls, nr_of_citizens: int) -> "Simulation":
        citizens = np.array([Citizen.random(citizen_id=i) for i in range(nr_of_citizens)])
        connectivity = initiate_connectivity_matrix(nr_of_citizens)

        logger.info(f"Initialized random simulation with {nr_of_citizens} citizens.")
        logger.debug(f"Citizens:\n{citizens}")
        logger.debug(f"Connectivity Matrix:\n{connectivity}")

        return cls(citizens, connectivity)
    
    @classmethod
    def load(cls, filepath: str) -> "Simulation":
        with open(filepath, 'rb') as f:
            citizens_history, connectivity_history = pickle.load(f)

        last_citizens = citizens_history[-1]
        last_connectivity = connectivity_history[-1]

        logger.info(f"Loaded simulation from {filepath}")
        logger.info(f"Simulation had {len(last_citizens)} citizens")
        logger.info(f"Simulation lasted for {len(citizens_history) - 1} iterations")
        logger.info(f"Simulation lasted {iterations_to_simtime(len(citizens_history) - 1).years} years and {iterations_to_simtime(len(citizens_history) - 1).months} months")
        logger.debug(f"Citizens:\n{last_citizens}")
        logger.debug(f"Connectivity Matrix:\n{last_connectivity}")

        recover_simulation = cls(last_citizens, last_connectivity)
        recover_simulation.citizens_history = citizens_history
        recover_simulation.connectivity_matrix_history = connectivity_history
        recover_simulation.iterations = len(citizens_history) - 1

        return recover_simulation