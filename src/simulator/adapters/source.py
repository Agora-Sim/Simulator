# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Source:
    simulation_name: str
    simulation_description: str
    folder: Path

    @property
    def runs_folder(self):
        return self.folder / "runs"

    def get_run_folder(self, run_id: str) -> Path:
        return self.runs_folder / run_id
