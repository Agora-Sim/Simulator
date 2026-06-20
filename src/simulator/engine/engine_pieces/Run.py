# ================================================================
# 0. Section: Imports
# ================================================================
from copy import deepcopy

from .Summary import Summary
from .Saver import Saver
from ..utils import age_citizens



# ================================================================
# 1. Section: Run Class
# ================================================================
class Run(Summary, Saver):
    def run_step(self) -> None:
        age_citizens(self.citizens)

        self.iterations += 1
        self.citizens_history.append(deepcopy(self.citizens))
        self.connectivity_matrix_history.append(deepcopy(self.connectivity_matrix))

    def run(self) -> None:
        while any(citizen.state == "alive" for citizen in self.citizens): 
            self.run_step()

        self.summary()
        self.save_run()