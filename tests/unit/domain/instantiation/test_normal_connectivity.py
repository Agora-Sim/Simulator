"""Contract tests for NormalConnectivity.

NormalConnectivity exposes the mean/std of its config dict and declares the
class-level connectivity type "normal". build() draws a connectivity row shaped
like the node row it is given.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.instantiation.normal_connectivity import NormalConnectivity


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_type_is_normal() -> None:
    assert NormalConnectivity.type == "normal"


@pytest.mark.unit
def test_mean_and_std_read_from_data() -> None:
    rule = NormalConnectivity(data={"type": "normal", "mean": 3.0, "std": 0.5})

    assert rule.mean == 3.0
    assert rule.std == 0.5


@pytest.mark.unit
def test_build_returns_row_matching_node_row_shape() -> None:
    rule = NormalConnectivity(data={"type": "normal", "mean": 1.0, "std": 1.0})

    row = rule.build(node_id=0, node_row=np.zeros(3))

    assert row.shape == (3,)
