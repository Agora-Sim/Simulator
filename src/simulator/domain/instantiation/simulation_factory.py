"""Simulation factory for building a runnable Simulation.

This module defines SimulationFactory. It is used to turn a
SimulationBlueprint into a fully wired Simulation, ready to be run.

Main components:
    SimulationFactory: builds a Simulation from a SimulationBlueprint.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass, field

from .node_factory import NodeFactory
from .simulation_blueprint import SimulationBlueprint
from ..simulation_engine import SimulationEngine
from ...service.simulation_run import SimulationRun


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationFactory:
    """Build a runnable Simulation from a SimulationBlueprint.

    SimulationFactory is responsible for turning simulation configuration
    into a fully wired Simulation, delegating node and connectivity creation
    to NodeFactory. It should be used once per simulation setup, before
    calling Simulation.run_simulation().

    Attributes:
        _node_factory: NodeFactory
            Factory used to build nodes and connectivity.
    """

    _node_factory: NodeFactory = field(default_factory=NodeFactory)

    def build_simulation(self, blueprint: SimulationBlueprint) -> SimulationRun:
        node_blueprint = blueprint.node_blueprint
        simulation_specs = blueprint.simulation_specs

        nodes = self._node_factory.build_nodes(node_blueprint)
        connectivity_matrix = self._node_factory.build_connectivity_matrix(
            nodes, node_blueprint
        )

        engine = SimulationEngine(
            nodes=nodes,
            connectivity_matrix=connectivity_matrix,
            simulation_specs=simulation_specs,
        )

        return SimulationRun(engine=engine)
