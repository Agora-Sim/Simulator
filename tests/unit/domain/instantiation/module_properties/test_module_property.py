"""Contract tests for ModuleProperty.

ModuleProperty is a view over a single module's config. Its `variables` property
maps each variable name to a VariableProperty wrapping that variable's config.
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
    prop = ModuleProperty(name="health", data=_module_data())

    assert prop.name == "health"
    assert prop.data == _module_data()


@pytest.mark.unit
def test_variables_keys_match_variable_names() -> None:
    prop = ModuleProperty(name="health", data=_module_data())

    assert set(prop.variables.keys()) == {"health", "age"}


@pytest.mark.unit
def test_variables_is_empty_for_module_without_variables() -> None:
    prop = ModuleProperty(name="empty_module", data={})

    assert prop.variables == {}


@pytest.mark.unit
def test_variables_values_are_variable_properties() -> None:
    prop = ModuleProperty(name="health", data=_module_data())

    assert all(isinstance(v, VariableProperty) for v in prop.variables.values())
