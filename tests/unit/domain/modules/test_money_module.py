"""Contract tests for MoneyModule."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.modules import MoneyModule
from simulator.domain.simulation_state import SimulationState

# apply() must ignore its inputs entirely, so null stand-ins are passed on
# purpose: any access would raise and fail the test.
_NULL_STATE = cast(SimulationState, None)
_NULL_RNG = cast(np.random.Generator, None)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_money_module_name_is_class_level() -> None:
    assert MoneyModule.name == "money"


@pytest.mark.unit
def test_money_module_stores_fields() -> None:
    module = MoneyModule(balance=1000.0, income=250.0)

    assert module.balance == 1000.0
    assert module.income == 250.0


@pytest.mark.unit
def test_apply_returns_no_effects() -> None:
    # The engine extends its effect list with apply()'s return value, so a
    # passive module must return an empty list, never None.
    module = MoneyModule(balance=1000.0, income=250.0)

    assert module.apply(_NULL_STATE, _NULL_RNG) == []
