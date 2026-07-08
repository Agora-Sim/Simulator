"""Fake collaborators for service-layer tests.

The service layer (Simulation) orchestrates a SimulationEngine. We drive it with
a lightweight recording fake rather than a real engine so the test stays fast,
deterministic and independent of the (not-yet-implemented) engine internals.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FakeSimulationSpecs:
    """Minimal stand-in exposing only what Simulation reads."""

    max_duration: int


class RecordingEngine:
    """A SimulationEngine-shaped fake that records how often step() is called.

    Each call to step() returns a distinct sentinel state and increments a
    counter, letting tests assert on the number of steps taken and the collected
    history without depending on real node/connectivity logic.
    """

    def __init__(self, max_duration: int) -> None:
        self.simulation_specs = FakeSimulationSpecs(max_duration=max_duration)
        self.step_calls = 0

    def step(self) -> str:
        state = f"state-{self.step_calls}"
        self.step_calls += 1
        return state
