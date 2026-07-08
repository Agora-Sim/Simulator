"""Contract tests for ResourceProperty.

ResourceProperty subclasses ABC but does not mark apply() as abstract; instead
apply() raises NotImplementedError until a concrete property overrides it.
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
def test_resource_property_apply_raises_not_implemented() -> None:
    prop = ResourceProperty()

    with pytest.raises(NotImplementedError, match="apply method must be implemented"):
        prop.apply()


@pytest.mark.unit
def test_subclass_can_override_apply() -> None:
    class Concrete(ResourceProperty):
        name = "concrete"

        def apply(self) -> str:
            return "applied"

    assert Concrete().apply() == "applied"
