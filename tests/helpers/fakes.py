"""Fake collaborators for service-layer tests.

The service layer (Simulation) orchestrates a SimulationEngine. We drive it with
a lightweight recording fake rather than a real engine so the test stays fast,
deterministic and independent of the (not-yet-implemented) engine internals.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FakeStepType:
    """Minimal stand-in for StepType exposing only the ``factor`` Simulation reads."""

    factor: float = 1.0
    unit: str = "step"


@dataclass
class FakeSimulationSpecs:
    """Minimal stand-in exposing only what Simulation reads."""

    max_duration: int
    step_size: FakeStepType = field(default_factory=FakeStepType)


class RecordingEngine:
    """A SimulationEngine-shaped fake that records how often step() is called.

    Each call to step() returns a distinct sentinel state and increments a
    counter, letting tests assert on the number of steps taken and the collected
    history without depending on real node/connectivity logic. The ``current_step``
    passed by Simulation is recorded so tests can assert on time advancement.
    """

    def __init__(self, max_duration: int, step_factor: float = 1.0) -> None:
        self.simulation_specs = FakeSimulationSpecs(
            max_duration=max_duration,
            step_size=FakeStepType(factor=step_factor),
        )
        self.step_calls = 0
        self.step_args: list[float] = []

    def step(self, current_step: float) -> str:
        self.step_args.append(current_step)
        state = f"state-{self.step_calls}"
        self.step_calls += 1
        return state
