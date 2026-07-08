"""Contract tests for VariableProperty.

VariableProperty is a view over a single variable's config. It exposes a
PropertyRange (from "range") and a PropertyDistribution (dispatched by
"distribution.type"), and samples a value via that distribution.

NOTE: the normal-distribution path is currently broken (see the xfail tests):
`distribution` builds ``NormalDistribution(**data["distribution"])``, spreading
``type``/``mean``/``std`` as keyword arguments, but the dataclass only accepts a
single ``data`` field. These tests encode the *intended* contract so they start
passing automatically once the constructor call is fixed.
"""

import random

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


def _variable_data(mean: float = 50.0, std: float = 5.0):
    return {
        "range": [0.0, 100.0],
        "distribution": {"type": "normal", "mean": mean, "std": std},
    }


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


@pytest.mark.xfail(
    reason="distribution builds NormalDistribution(**dict) with extra kwargs; "
    "the dataclass only accepts `data`.",
    strict=True,
)
@pytest.mark.unit
def test_distribution_normal_returns_normal_distribution() -> None:
    prop = VariableProperty(data=_variable_data(mean=3.0, std=1.0))

    distribution = prop.distribution

    assert isinstance(distribution, NormalDistribution)
    assert distribution.mean == 3.0
    assert distribution.std == 1.0


@pytest.mark.xfail(
    reason="sample() delegates to the broken distribution property.",
    strict=True,
)
@pytest.mark.unit
def test_sample_returns_float_from_distribution() -> None:
    prop = VariableProperty(data=_variable_data(mean=0.0, std=1.0))

    random.seed(0)
    value = prop.sample()

    assert isinstance(value, float)
