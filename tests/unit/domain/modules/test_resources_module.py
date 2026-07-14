"""Contract tests for ResourcesModule."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.modules import ResourcesModule
from simulator.domain.modules.resource import Resource
from simulator.domain.simulation_state import SimulationState

# apply() must ignore its inputs entirely, so null stand-ins are passed on
# purpose: any access would raise and fail the test.
_NULL_STATE = cast(SimulationState, None)
_NULL_RNG = cast(np.random.Generator, None)


# ================================================================
# 1. Section: Fixtures
# ================================================================
def _resource(name: str = "wheat") -> Resource:
    return Resource(
        name=name,
        sell_value=10.0,
        target_value=100.0,
        consume_rate=1.0,
        production_rate=2.0,
        properties=[],
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_resources_module_name_is_class_level() -> None:
    assert ResourcesModule.name == "resources_module"


@pytest.mark.unit
def test_resources_module_stores_resources() -> None:
    resources = [_resource("wheat"), _resource("iron")]

    module = ResourcesModule(resources=resources)

    assert module.resources == resources


@pytest.mark.unit
def test_resources_module_accepts_empty_resource_list() -> None:
    module = ResourcesModule(resources=[])

    assert module.resources == []


@pytest.mark.unit
def test_apply_returns_no_effects() -> None:
    # The engine extends its effect list with apply()'s return value, so a
    # passive module must return an empty list, never None.
    module = ResourcesModule(resources=[_resource()])

    assert module.apply(_NULL_STATE, _NULL_RNG) == []
