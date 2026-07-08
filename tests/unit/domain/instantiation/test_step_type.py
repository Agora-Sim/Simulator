"""Contract tests for StepType.

StepType parses a "<factor> <unit>" string into a numeric factor and a unit
label, e.g. "1.0 months" -> StepType(factor=1.0, unit="months").
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.step_type import StepType


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_step_type_stores_fields() -> None:
    step = StepType(factor=2.5, unit="days")

    assert step.factor == 2.5
    assert step.unit == "days"


@pytest.mark.unit
@pytest.mark.parametrize(
    "text, expected_factor, expected_unit",
    [
        ("1.0 months", 1.0, "months"),
        ("0.5 days", 0.5, "days"),
        ("12 hours", 12.0, "hours"),
        ("3 years", 3.0, "years"),
    ],
)
def test_from_str_parses_factor_and_unit(text, expected_factor, expected_unit) -> None:
    step = StepType.from_str(text)

    assert step.factor == expected_factor
    assert step.unit == expected_unit


@pytest.mark.unit
def test_from_str_factor_is_a_float() -> None:
    step = StepType.from_str("7 days")

    assert isinstance(step.factor, float)
    assert step.factor == 7.0


@pytest.mark.unit
def test_from_str_rejects_string_without_unit() -> None:
    # "1.0" splits into a single token, so unpacking into (factor, unit) fails.
    with pytest.raises(ValueError):
        StepType.from_str("1.0")


@pytest.mark.unit
def test_from_str_rejects_non_numeric_factor() -> None:
    with pytest.raises(ValueError):
        StepType.from_str("abc months")
