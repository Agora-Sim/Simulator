"""Contract tests for MoneyModule."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules import MoneyModule


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
