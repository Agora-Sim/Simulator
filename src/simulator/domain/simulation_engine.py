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

    def step(
        self,
        current_step: float,
        previous_state: SimulationState,
        rng: np.random.Generator,
    ) -> SimulationState:
        effects = []
        for node in self.nodes:
            node_effects = self.step_node(node, previous_state, rng)
            effects.extend(node_effects)

        simulation_state = SimulationState(
            nodes=self.nodes,
            connectivity_matrix=self.connectivity_matrix,
            time_idx=current_step,
            time_step=self.simulation_specs.step_size,
        )

        self.reduce(simulation_state, effects)
        self.update_from_state(simulation_state)

        return simulation_state


    # ──────────────────────────────────────────────────────
    # 1.1 Subsection: Helper Functions
    # ──────────────────────────────────────────────────────
    def step_node(
        self, node: Node, previous_state: SimulationState, rng: np.random.Generator
    ) -> list:
        node_effects = []
        for module in node.modules:
            effects = self.step_module(module, previous_state, rng)
            node_effects.extend(effects)

        return node_effects

    def step_module(
        self,
        module: NodeModule,
        previous_state: SimulationState,
        rng: np.random.Generator,
    ) -> list:
        effects = module.apply(previous_state, rng)

        return effects


    # ──────────────────────────────────────────────────────
    # 1.1 Subsection: Helper Functions
    # ──────────────────────────────────────────────────────
    def build_state(self) -> SimulationState:
        return SimulationState(
            nodes=self.nodes,
            connectivity_matrix=self.connectivity_matrix,
            time_idx=-1,
            time_step=self.simulation_specs.step_size,
        )


    # ──────────────────────────────────────────────────────
    # 1.1 Subsection: Helper Functions
    # ──────────────────────────────────────────────────────
    def reduce(self, state: SimulationState, effects: list) -> None:
        for effect in sorted(effects, key=lambda effect: effect.priority):
            effect.apply(state)

    def update_from_state(self, state: SimulationState) -> None:
        self.nodes = state.nodes
        self.connectivity_matrix = state.connectivity_matrix
