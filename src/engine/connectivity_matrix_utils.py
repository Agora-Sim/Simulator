import numpy as np

def initiate_connectivity_matrix(nr_of_citizens: int) -> np.ndarray:
    return np.zeros((nr_of_citizens, nr_of_citizens))