"""Simulation runner for executing a full simulation.

This module defines Simulation, the service-layer entry point that drives a
simulation run to completion. It is used by client code to execute a
configured SimulationEngine and collect the resulting history.

Main components:
    Simulation: runs a SimulationEngine until the configured duration ends.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass, field

from ..domain.simulation_engine import SimulationEngine
from ..domain.simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Simulation:
    """Run a SimulationEngine to completion and collect its history.

    Simulation is responsible for repeatedly stepping a SimulationEngine
    until the configured max duration is reached. It should be used as the
    main entry point to execute a simulation run. It should not be
    responsible for building the engine or its nodes, that responsibility
    belongs to SimulationFactory.

    Attributes:
        engine: SimulationEngine
            The engine driving the simulation.
    """

    engine: SimulationEngine

    _current_step: int = field(default=0, init=False)
    _history: list[SimulationState] = field(default_factory=list, init=False)

    def run_simulation(self) -> None:
        max_duration = self.engine.simulation_specs.max_duration

        while self._current_step < max_duration:
            state = self.engine.step()
            self._history.append(state)
            self._current_step += 1
