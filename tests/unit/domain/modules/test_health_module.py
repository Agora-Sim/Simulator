"""Contract tests for HealthModule."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules import HealthModule


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_health_module_name_is_class_level() -> None:
    assert HealthModule.name == "health"


@pytest.mark.unit
def test_health_module_stores_fields() -> None:
    module = HealthModule(health=90.0, age=42.0)

    assert module.health == 90.0
    assert module.age == 42.0
