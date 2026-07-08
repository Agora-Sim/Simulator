"""Contract tests for PropertyRange.

PropertyRange is a frozen value object holding a [min, max] pair. It can be built
from a two-element list and rejects ranges where min > max.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import dataclasses

import pytest

from simulator.domain.instantiation.module_properties.property_range import (
    PropertyRange,
)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_stores_min_and_max() -> None:
    prop_range = PropertyRange(min=0.0, max=10.0)

    assert prop_range.min == 0.0
    assert prop_range.max == 10.0


@pytest.mark.unit
def test_from_list_builds_from_two_values() -> None:
    prop_range = PropertyRange.from_list([2.0, 8.0])

    assert prop_range.min == 2.0
    assert prop_range.max == 8.0


@pytest.mark.unit
def test_equal_min_and_max_is_allowed() -> None:
    prop_range = PropertyRange(min=5.0, max=5.0)

    assert prop_range.min == prop_range.max == 5.0


@pytest.mark.unit
def test_min_greater_than_max_raises_value_error() -> None:
    with pytest.raises(ValueError, match="min cannot be greater than max"):
        PropertyRange(min=10.0, max=1.0)


@pytest.mark.unit
def test_from_list_with_inverted_values_raises_value_error() -> None:
    with pytest.raises(ValueError, match="min cannot be greater than max"):
        PropertyRange.from_list([9.0, 3.0])


@pytest.mark.unit
def test_is_frozen() -> None:
    prop_range = PropertyRange(min=0.0, max=1.0)

    with pytest.raises(dataclasses.FrozenInstanceError):
        prop_range.min = 5.0  # type: ignore[misc]
