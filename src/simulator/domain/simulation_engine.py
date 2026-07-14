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
import numpy as np

from dataclasses import dataclass

from .node import Node
from .modules import NodeModule
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

    def step(self, current_step: float, rng: np.random.Generator) -> SimulationState:
        nodes = []
        for node in self.nodes:
            node = self.step_node(node, rng)
            nodes.append(node)

        simulation_state = SimulationState(
            nodes=nodes,
            connectivity_matrix=self.connectivity_matrix,
            time_idx=current_step,
        )

        return simulation_state

    def step_node(self, node: Node, rng: np.random.Generator) -> Node:
        for idx, module in enumerate(node.modules):
            module = self.step_module(module, rng)
            node.modules[idx] = module

        return node

    def step_module(self, module: NodeModule, rng: np.random.Generator) -> NodeModule:
        module.apply(rng)

        return module
