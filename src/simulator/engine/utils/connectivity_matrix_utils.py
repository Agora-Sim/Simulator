# ================================================================
# 0. Section: Imports
# ================================================================
import numpy as np



# ================================================================
# 1. Section: Initiators of Connectivity Matrix
# ================================================================
def initiate_connectivity_matrix(nr_of_citizens: int) -> np.ndarray:
    return np.zeros((nr_of_citizens, nr_of_citizens))