"""Contract tests for the x axis Metric derives from the simulation specs.

Every Metric builds its own x axis from SimulationSpecs rather than letting
RunAggregator compute timepoints: the values span max_duration + 1 steps
scaled by the step factor, and the unit is carried over from step_size so
downstream plots can label and range-share on it.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pytest

from simulator.domain.analysis import Axis
from simulator.domain.analysis.metrics import AgeMetric

from tests.helpers.builders import build_simulation_specs


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_x_axis_is_labelled_time_in_the_step_unit() -> None:
    specs = build_simulation_specs(step_size="1.0 months")

    axis = AgeMetric(unit="years").x_axis(specs)

    assert isinstance(axis, Axis)
    assert axis.label == "Time"
    assert axis.unit == "months"


@pytest.mark.unit
def test_x_axis_spans_one_value_per_step_plus_the_initial_state() -> None:
    specs = build_simulation_specs(max_duration=3, step_size="1.0 months")

    axis = AgeMetric(unit="years").x_axis(specs)

    np.testing.assert_array_equal(axis.values, np.array([0.0, 1.0, 2.0, 3.0]))


@pytest.mark.unit
def test_x_axis_values_are_scaled_by_the_step_factor() -> None:
    specs = build_simulation_specs(max_duration=3, step_size="0.5 days")

    axis = AgeMetric(unit="years").x_axis(specs)

    np.testing.assert_array_equal(axis.values, np.array([0.0, 0.5, 1.0, 1.5]))
