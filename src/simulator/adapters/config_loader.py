# ================================================================
# 0. Section: IMPORTS
# ================================================================
import yaml

from dataclasses import dataclass

from .source import Source
from ..domain.instantiation.simulation_blueprint import SimulationBlueprint


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ConfigLoader:
    source: Source

    def load_config(self) -> SimulationBlueprint:
        path = self.source.config_path

        with open(path, "r", encoding="utf-8") as f:
            payload = yaml.safe_load(f)

        return SimulationBlueprint(payload)
