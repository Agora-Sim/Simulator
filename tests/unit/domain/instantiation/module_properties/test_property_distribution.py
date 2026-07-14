"""Contract tests for the PropertyDistribution abstract base."""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.instantiation.module_properties.property_distribution import (
    PropertyDistribution,
)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_property_distribution_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        PropertyDistribution(data={})  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_must_implement_sample() -> None:
    class Incomplete(PropertyDistribution):
        type = "incomplete"

    with pytest.raises(TypeError):
        Incomplete(data={})  # type: ignore[abstract]


@pytest.mark.unit
def test_subclass_with_sample_can_be_instantiated() -> None:
    class Constant(PropertyDistribution):
        type = "constant"

        def sample(self, rng) -> float:
            return 1.5

    assert Constant(data={}).sample(np.random.default_rng(0)) == 1.5
