"""Contract tests for the Simulation service.

Simulation drives a SimulationEngine, calling step() until the engine's
configured max_duration is reached and collecting each returned state into its
history. We use a RecordingEngine fake so the test is fast and independent of the
(unimplemented) real engine step logic.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.service.simulation import Simulation
from tests.helpers.fakes import RecordingEngine


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_run_simulation_steps_engine_max_duration_times() -> None:
    engine = RecordingEngine(max_duration=5)
    simulation = Simulation(engine=engine)

    simulation.run_simulation()

    assert engine.step_calls == 5


@pytest.mark.unit
def test_run_simulation_collects_one_state_per_step() -> None:
    engine = RecordingEngine(max_duration=3)
    simulation = Simulation(engine=engine)

    simulation.run_simulation()

    # History is the documented output of a run: one state per step, in order.
    assert simulation._history == ["state-0", "state-1", "state-2"]


@pytest.mark.unit
def test_run_simulation_advances_current_step_to_max_duration() -> None:
    engine = RecordingEngine(max_duration=4)
    simulation = Simulation(engine=engine)

    simulation.run_simulation()

    assert simulation._current_step == 4


@pytest.mark.unit
def test_run_simulation_with_zero_duration_does_nothing() -> None:
    engine = RecordingEngine(max_duration=0)
    simulation = Simulation(engine=engine)

    simulation.run_simulation()

    assert engine.step_calls == 0
    assert simulation._history == []


@pytest.mark.unit
def test_simulation_starts_with_empty_history_before_running() -> None:
    simulation = Simulation(engine=RecordingEngine(max_duration=2))

    assert simulation._history == []
    assert simulation._current_step == 0
