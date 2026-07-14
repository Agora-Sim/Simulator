"""Contract tests for the Simulation service.

Simulation drives a SimulationEngine, calling step() until the engine's
configured max_duration is reached and collecting each returned state into its
history. We use a RecordingEngine fake so the test is fast and independent of
the real engine step logic.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.simulation_engine import SimulationEngine
from simulator.service.simulation_run import SimulationRun
from tests.helpers.fakes import RecordingEngine

# A shared throwaway generator; these tests use a no-op RecordingEngine
_RNG = np.random.default_rng(0)


def _simulation(engine: RecordingEngine) -> SimulationRun:
    """Wire the engine-shaped fake into a SimulationRun."""
    return SimulationRun(engine=cast(SimulationEngine, engine))


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_run_simulation_steps_engine_max_duration_times() -> None:
    engine = RecordingEngine(max_duration=5)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    assert engine.step_calls == 5


@pytest.mark.unit
def test_run_simulation_collects_one_state_per_step() -> None:
    engine = RecordingEngine(max_duration=3)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    # History is the documented output of a run: the initial state recorded
    # before stepping, then one state per step, in order.
    assert simulation.history == ["initial-state", "state-0", "state-1", "state-2"]


@pytest.mark.unit
def test_run_simulation_advances_current_step_to_max_duration() -> None:
    engine = RecordingEngine(max_duration=4)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    assert simulation.current_step == 4


@pytest.mark.unit
def test_run_simulation_with_zero_duration_takes_no_steps() -> None:
    engine = RecordingEngine(max_duration=0)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    # No steps are taken, but the initial state is still recorded.
    assert engine.step_calls == 0
    assert simulation.history == ["initial-state"]


@pytest.mark.unit
def test_simulation_starts_with_empty_history_before_running() -> None:
    simulation = _simulation(RecordingEngine(max_duration=2))

    assert simulation.history == []
    assert simulation.current_step == 0


@pytest.mark.unit
def test_run_simulation_passes_current_step_to_engine() -> None:
    engine = RecordingEngine(max_duration=3)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    # Each step() receives the current time index before it is advanced.
    assert engine.step_args == [0, 1, 2]


@pytest.mark.unit
def test_run_simulation_advances_by_step_factor() -> None:
    # A fractional step factor means more steps are taken to reach max_duration
    # and time advances in factor-sized increments.
    engine = RecordingEngine(max_duration=2, step_factor=0.5)
    simulation = _simulation(engine)

    simulation.run_simulation(_RNG)

    assert engine.step_calls == 4
    assert engine.step_args == [0.0, 0.5, 1.0, 1.5]
    assert simulation.current_step == 2.0
