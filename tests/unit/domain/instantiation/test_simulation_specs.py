"""Contract tests for SimulationSpecs.

SimulationSpecs is a typed read-only view over the raw "simulation" config dict.
Each property exposes one config value; step_size is parsed into a StepType.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.step_type import StepType
from simulator.domain.instantiation.simulation_specs import SimulationSpecs
from tests.helpers.builders import build_simulation_data


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_exposes_scalar_specs() -> None:
    specs = SimulationSpecs(
        build_simulation_data(
            max_duration=100, re_connection=False, seed=7, step_size="2 days"
        )
    )

    assert specs.max_duration == 100
    assert specs.re_connection is False
    assert specs.seed == 7


@pytest.mark.unit
def test_step_size_is_parsed_into_step_type() -> None:
    specs = SimulationSpecs(build_simulation_data(step_size="1.0 months"))

    assert specs.step_size == StepType(factor=1.0, unit="months")


@pytest.mark.unit
def test_missing_key_raises_key_error() -> None:
    specs = SimulationSpecs({})

    with pytest.raises(KeyError):
        _ = specs.max_duration
