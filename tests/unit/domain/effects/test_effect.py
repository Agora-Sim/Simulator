"""Contract tests for the Effect abstract base.

Effect is the command object modules emit to mutate the world: it declares
`name`/`priority` class variables and an abstract apply(state). The contract
worth pinning is that it cannot be instantiated directly and that concrete
subclasses must supply apply().
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.effects import Effect


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_effect_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        Effect()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_without_apply_cannot_be_instantiated() -> None:
    class Incomplete(Effect):
        pass

    with pytest.raises(TypeError):
        Incomplete()  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_with_apply_can_be_instantiated() -> None:
    class Concrete(Effect):
        name = "concrete"
        priority = 0

        def apply(self, state) -> None:
            pass

    Concrete()
