# ================================================================
# 0. Section: Imports
# ================================================================
import os
import pickle

import datetime

from ...logger import logger



# ================================================================
# 1. Section: Saving Class
# ================================================================
class Saver:
    def save_run(self, output_path: str = 'runs') -> None:
        os.makedirs(output_path, exist_ok=True)

        date_hour = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_run_{date_hour}.pkl"
        filepath = os.path.join(output_path, filename)

        run = [self.citizens_history, self.connectivity_matrix_history]

        with open(filepath, 'wb') as f:
            pickle.dump(run, f)

        logger.info(f"Simulation run saved to {filepath}.")
