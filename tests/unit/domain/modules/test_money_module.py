"""Contract tests for MoneyModule."""

import pytest

from simulator.domain.modules import MoneyModule


@pytest.mark.unit
def test_money_module_name_is_class_level() -> None:
    assert MoneyModule.name == "money_module"


@pytest.mark.unit
def test_money_module_stores_fields() -> None:
    module = MoneyModule(balance=1000.0, income=250.0)

    assert module.balance == 1000.0
    assert module.income == 250.0


@pytest.mark.unit
def test_money_module_apply_is_noop_returning_none() -> None:
    module = MoneyModule(balance=1000.0, income=250.0)

    assert module.apply() is None
