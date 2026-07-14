"""Contract tests for the NodeModule abstract base.

NodeModule is an abstract dataclass: it declares a `name` class variable and an
abstract apply() method. The contract worth pinning is that it cannot be
instantiated directly and that concrete subclasses must supply apply().
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules.node_module import NodeModule


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_node_module_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        NodeModule()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_without_apply_cannot_be_instantiated() -> None:
    class Incomplete(NodeModule):
        pass

    with pytest.raises(TypeError):
        Incomplete()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_with_apply_can_be_instantiated() -> None:
    class Concrete(NodeModule):
        name = "concrete"

        def apply(self, rng) -> str:
            return "applied"

    module = Concrete()

    assert module.apply(None) == "applied"
