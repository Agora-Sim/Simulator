# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from dataclasses import dataclass

from .variable_property import VariableProperty


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ModuleProperty:
    name: str
    data: dict[str, Any]

    @property
    def variables(self) -> dict[str, VariableProperty]:
        variables = {}

        for variable_name, variable_data in self.data.items():
            variables[variable_name] = VariableProperty(variable_data)

        return variables
