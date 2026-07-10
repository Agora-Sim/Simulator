"""Contract tests for ConnectivityMatrix.

ConnectivityMatrix wraps a numpy array of pairwise connectivity. Its
get_most_connected() behaviour is not implemented yet, so it is intentionally
left untested until real logic lands.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.connectivity_matrix import ConnectivityMatrix


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_connectivity_matrix_stores_data() -> None:
    data = np.array([[0.0, 1.0], [1.0, 0.0]])

    matrix = ConnectivityMatrix(data=data)

    np.testing.assert_array_equal(matrix.data, data)
