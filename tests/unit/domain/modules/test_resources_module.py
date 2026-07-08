"""Contract tests for ResourcesModule."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules import ResourcesModule
from simulator.domain.modules.resource import Resource


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
def test_resources_module_apply_is_noop_returning_none() -> None:
    module = ResourcesModule(resources=[_resource()])

    assert module.apply() is None
