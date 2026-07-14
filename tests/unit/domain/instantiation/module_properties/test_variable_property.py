"""Contract tests for VariableProperty.

VariableProperty is a view over a single variable's config. It exposes a
PropertyRange (from "range") and a PropertyDistribution (dispatched by
"distribution.type"), and samples a value via that distribution.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.instantiation.module_properties.property_range import (
    PropertyRange,
)
from simulator.domain.instantiation.module_properties.normal_distribution import (
    NormalDistribution,
)
from simulator.domain.instantiation.module_properties.variable_property import (
    VariableProperty,
)


# ================================================================
# 1. Section: Fixtures
# ================================================================
def _variable_data(mean: float = 50.0, std: float = 5.0):
    return {
        "range": [0.0, 100.0],
        "distribution": {"type": "normal", "mean": mean, "std": std},
    }


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_range_is_built_from_range_list() -> None:
    prop = VariableProperty(data=_variable_data())

    assert prop.range == PropertyRange(min=0.0, max=100.0)


@pytest.mark.unit
def test_distribution_unknown_type_raises_value_error() -> None:
    prop = VariableProperty(
        data={"range": [0.0, 1.0], "distribution": {"type": "poisson"}}
    )

    with pytest.raises(ValueError, match="Unknown distribution type: poisson"):
        _ = prop.distribution


@pytest.mark.unit
def test_distribution_normal_returns_normal_distribution() -> None:
    prop = VariableProperty(data=_variable_data(mean=3.0, std=1.0))

    distribution = prop.distribution

    assert isinstance(distribution, NormalDistribution)
    assert distribution.mean == 3.0
    assert distribution.std == 1.0


@pytest.mark.unit
def test_sample_returns_float_from_distribution() -> None:
    prop = VariableProperty(data=_variable_data(mean=0.0, std=1.0))

    value = prop.sample(np.random.default_rng(0))

    assert isinstance(value, float)
