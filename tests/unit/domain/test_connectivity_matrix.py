"""Contract tests for ConnectivityMatrix.

ConnectivityMatrix wraps a numpy array of pairwise connectivity. Its
get_most_connected() behaviour is not implemented yet; the test below pins its
current contract so a future implementation announces itself by failing.
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


@pytest.mark.unit
def test_get_most_connected_is_not_implemented_yet() -> None:
    # Current behaviour: the method body is a bare `pass`, returning None.
    # This test documents that contract and will fail once real logic lands,
    # prompting an update.
    matrix = ConnectivityMatrix(data=np.zeros((3, 3)))

    assert matrix.get_most_connected() is None
