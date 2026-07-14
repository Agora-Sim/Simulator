"""Contract tests for the NodeModule abstract base.

NodeModule is an abstract dataclass: it declares a `name` class variable, a
`node_id` stamped by the owning Node (never passed at construction) and an
abstract apply(previous_state, rng) that returns the effects the module wants
applied to the world.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.modules.node_module import NodeModule
from simulator.domain.simulation_state import SimulationState

# apply() must ignore its inputs entirely, so null stand-ins are passed on
# purpose: any access would raise and fail the test.
_NULL_STATE = cast(SimulationState, None)
_NULL_RNG = cast(np.random.Generator, None)


# ================================================================
# 1. Section: Fixtures
# ================================================================
class Concrete(NodeModule):
    name = "concrete"

    def apply(self, previous_state, rng) -> list:
        return []


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_node_module_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        NodeModule()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_without_apply_cannot_be_instantiated() -> None:
    class Incomplete(NodeModule):
        pass

    with pytest.raises(TypeError):
        Incomplete()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_with_apply_can_be_instantiated() -> None:
    module = Concrete()

    assert module.apply(_NULL_STATE, _NULL_RNG) == []


@pytest.mark.unit
def test_node_id_defaults_to_unassigned() -> None:
    module = Concrete()

    assert module.node_id == -1


@pytest.mark.unit
def test_node_id_is_not_a_constructor_argument() -> None:
    with pytest.raises(TypeError):
        Concrete(node_id=3)  # type: ignore[call-arg]
