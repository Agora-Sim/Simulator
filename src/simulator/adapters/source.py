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
    base_folder: Path = Path("data")

    def __post_init__(self):
        if self.folder.exists():
            self.simulation_name = (
                self.simulation_name + "_" + str(len(list(self.folder.iterdir())))
            )

    @property
    def folder(self):
        return self.base_folder / self.simulation_name

    @property
    def runs_folder(self):
        return self.folder / "runs"

    def get_run_folder(self, run_id: str) -> Path:
        return self.runs_folder / run_id
