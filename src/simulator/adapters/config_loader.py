# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from ruamel.yaml import YAML

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

        # typ="safe" loads plain dict/list, like PyYAML's safe_load.
        yaml = YAML(typ="safe")
        with open(path, "r", encoding="utf-8") as f:
            payload = yaml.load(f)

        return SimulationBlueprint(payload)
