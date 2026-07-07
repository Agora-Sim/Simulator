# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from .node_blueprint import NodeBlueprint
from .simulation_specs import SimulationSpecs


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationBlueprint:
    data: dict

    @property
    def node_blueprint(self) -> NodeBlueprint:
        if "nodes" not in self.data.keys():
            raise ValueError("'nodes' key not found in data")

        return NodeBlueprint(self.data["nodes"])

    @property
    def simulation_specs(self) -> SimulationSpecs:
        if "simulation" not in self.data.keys():
            raise ValueError("'simulation' key not found in data")

        return SimulationSpecs(self.data["simulation"])
