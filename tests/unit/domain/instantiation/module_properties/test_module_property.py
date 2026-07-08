"""Contract tests for ModuleProperty.

ModuleProperty is a view over a single module's config. Its `variables` property
is meant to map each variable name to a VariableProperty.

NOTE: `variables` currently returns the raw config dicts unchanged rather than
wrapping them in VariableProperty (its declared return type). The key mapping is
stable and tested directly; the wrapping contract is captured as an xfail so it
flips to passing once the wrapping is added.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.module_properties import (
    ModuleProperty,
)
from simulator.domain.instantiation.module_properties.variable_property import (
    VariableProperty,
)


# ================================================================
# 1. Section: Fixtures
# ================================================================
def _module_data():
    return {
        "health": {
            "range": [0, 100],
            "distribution": {"type": "normal", "mean": 50, "std": 5},
        },
        "age": {
            "range": [0, 100],
            "distribution": {"type": "normal", "mean": 30, "std": 2},
        },
    }


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_stores_name_and_data() -> None:
    prop = ModuleProperty(name="health_module", data=_module_data())

    assert prop.name == "health_module"
    assert prop.data == _module_data()


@pytest.mark.unit
def test_variables_keys_match_variable_names() -> None:
    prop = ModuleProperty(name="health_module", data=_module_data())

    assert set(prop.variables.keys()) == {"health", "age"}


@pytest.mark.unit
def test_variables_is_empty_for_module_without_variables() -> None:
    prop = ModuleProperty(name="empty_module", data={})

    assert prop.variables == {}


@pytest.mark.xfail(
    reason="variables returns raw config dicts instead of wrapping them in "
    "VariableProperty (its declared return type).",
    strict=True,
)
@pytest.mark.unit
def test_variables_values_are_variable_properties() -> None:
    prop = ModuleProperty(name="health_module", data=_module_data())

    assert all(isinstance(v, VariableProperty) for v in prop.variables.values())
