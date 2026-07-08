"""Contract tests for Resource."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules.resource import Resource


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_resource_stores_its_fields() -> None:
    resource = Resource(
        name="wheat",
        sell_value=12.5,
        target_value=100.0,
        consume_rate=1.5,
        production_rate=3.0,
        properties=[],
    )

    assert resource.name == "wheat"
    assert resource.sell_value == 12.5
    assert resource.target_value == 100.0
    assert resource.consume_rate == 1.5
    assert resource.production_rate == 3.0
    assert resource.properties == []


@pytest.mark.unit
def test_resources_with_equal_fields_are_equal() -> None:
    a = Resource("iron", 5.0, 50.0, 1.0, 1.0, [])
    b = Resource("iron", 5.0, 50.0, 1.0, 1.0, [])

    assert a == b
