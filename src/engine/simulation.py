# ================================================================
# 0. Section: Imports
# ================================================================
import numpy as np
from copy import deepcopy

from ..plots.plot_summary import plot_summary
from ..components import Citizen
from ..hyperparameters import INCLUDE_PLOTS

from .connectivity_matrix_utils import initiate_connectivity_matrix
from .citizens_utils import age_citizens

class Simulation:
    def __init__(self, citizens: np.ndarray, connectivity_matrix: np.ndarray):
        self.citizens = citizens
        self.connectivity_matrix = connectivity_matrix

        self.nr_of_citizens = len(citizens)
        self.iterations = 0
        self.citizens_history = [deepcopy(self.citizens)]



    # ================================================================
    # 1. Section: Initializers
    # ================================================================
    @classmethod
    def random(cls, nr_of_citizens: int):
        citizens = np.array([Citizen.random(citizen_id=i) for i in range(nr_of_citizens)])
        connectivity = initiate_connectivity_matrix(nr_of_citizens)
        return cls(citizens, connectivity)
    


    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def run_step(self):
        age_citizens(self.citizens)

    def run(self):
        while any(citizen.state == "alive" for citizen in self.citizens): 
            self.run_step()
            self.iterations += 1
            self.citizens_history.append(deepcopy(self.citizens))

        self.summary()

    def summary(self):
        print(f"Simulation ran for {self.iterations} iterations.")
        alive_count = sum(citizen.state == "alive" for citizen in self.citizens)
        dead_count = sum(citizen.state == "dead" for citizen in self.citizens)
        print(f"Final counts - Alive: {alive_count}, Dead: {dead_count}")

        plot_summary(self.citizens_history, include=INCLUDE_PLOTS)



    # ================================================================
    # 3. Section: Properties
    # ================================================================
    @property
    def nr_of_citizens(self):
        return self._nr_of_citizens
    @nr_of_citizens.setter
    def nr_of_citizens(self, value: int):
        if value <= 0:
            raise ValueError("Number of citizens must be positive.")
        self._nr_of_citizens = value

    @property
    def connectivity_matrix(self):
        return self._connectivity_matrix
    @connectivity_matrix.setter
    def connectivity_matrix(self, value: np.ndarray):
        self._connectivity_matrix = value

    @property
    def citizens(self):
        return self._citizens
    @citizens.setter
    def citizens(self, value: np.ndarray):
        self._citizens = value