"""Simulation engine for advancing simulation state.

This module defines SimulationEngine, the core computational unit of a
simulation run. It is used by Simulation to advance the node population and
connectivity matrix by one time step at a time.

Main components:
    SimulationEngine: advances nodes and connectivity by one simulation step.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .node import Node
from .connectivity_matrix import ConnectivityMatrix
from .simulation_state import SimulationState
from .instantiation.simulation_specs import SimulationSpecs


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationEngine:
    """Advance a population of nodes by one simulation step at a time.

    SimulationEngine is responsible for applying node module updates and
    producing the resulting SimulationState. It should be used by Simulation
    to drive a simulation run step by step. It should not be responsible for
    deciding when a simulation run stops, that belongs to Simulation.

    Attributes:
        nodes: list[Node]
            Nodes currently part of the simulation.
        connectivity_matrix: ConnectivityMatrix
            Connectivity between the simulation nodes.
        simulation_specs: SimulationSpecs
            Configuration specs for the simulation run.
    """

    nodes: list[Node]
    connectivity_matrix: ConnectivityMatrix
    simulation_specs: SimulationSpecs

    def step(self) -> SimulationState:
        raise NotImplementedError("step is not implemented")
