"""Contract tests for the ConnectivityRule abstract base."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.instantiation.connectivity import ConnectivityRule


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_connectivity_rule_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        ConnectivityRule(data={})  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_must_implement_build() -> None:
    class Incomplete(ConnectivityRule):
        type = "incomplete"

    with pytest.raises(TypeError):
        Incomplete(data={})  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_with_build_can_be_instantiated() -> None:
    class Concrete(ConnectivityRule):
        type = "concrete"

        def build(self, node_id: int, connection_dict: dict[str, list], rng):
            return np.array(connection_dict["candidates"])

    rule = Concrete(data={})
    connection_dict = {"already_connected": [], "candidates": [1, 2]}
    rng = np.random.default_rng(0)

    np.testing.assert_array_equal(rule.build(0, connection_dict, rng), [1, 2])
