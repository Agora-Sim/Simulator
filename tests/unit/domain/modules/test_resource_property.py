"""Contract tests for ResourceProperty.

ResourceProperty subclasses ABC but does not mark apply() as abstract; the base
apply() is not implemented yet, so only a concrete override is exercised here.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules.resource_property import ResourceProperty


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_subclass_can_override_apply() -> None:
    class Concrete(ResourceProperty):
        name = "concrete"

        def apply(self, rng) -> str:
            return "applied"

    assert Concrete().apply(None) == "applied"
