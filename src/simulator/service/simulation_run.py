"""Simulation runner for executing a full simulation.

This module defines SimulationRun, the service-layer entry point that drives a
simulation run to completion. It is used by client code to execute a
configured SimulationEngine and collect the resulting history.

Main components:
    SimulationRun: runs a SimulationEngine until the configured duration ends.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass, field

from ..domain.simulation_engine import SimulationEngine
from ..domain.simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationRun:
    """Run a SimulationEngine to completion and collect its history.

    SimulationRun is responsible for repeatedly stepping a SimulationEngine
    until the configured max duration is reached. It should be used as the
    main entry point to execute a simulation run. It should not be
    responsible for building the engine or its nodes, that responsibility
    belongs to SimulationFactory.

    Attributes:
        engine: SimulationEngine
            The engine driving the simulation.
    """

    engine: SimulationEngine

    current_step: float = field(default=0, init=False)
    history: list[SimulationState] = field(default_factory=list, init=False)

    def run_simulation(self, rng: np.random.Generator) -> None:
        max_duration = self.engine.simulation_specs.max_duration
        step_value = self.engine.simulation_specs.step_size.factor

        while self.current_step < max_duration:
            state = self.engine.step(self.current_step, rng)
            self.history.append(state)
            self.current_step += step_value
