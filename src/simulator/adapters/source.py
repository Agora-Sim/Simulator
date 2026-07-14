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

    @property
    def folder(self):
        return self.base_folder / self.simulation_name

    @property
    def runs_folder(self):
        return self.folder / "runs"

    @property
    def config_path(self) -> Path:
        return self.folder / "config.yaml"

    @property
    def figures_folder(self) -> Path:
        return self.folder / "figures"

    def get_run_folder(self, run_id: str) -> Path:
        return self.runs_folder / f"run_{run_id}"

    def get_figure_path(self, name: str, fmt: str) -> Path:
        return self.figures_folder / f"{name}.{fmt}"

    def get_nr_runs_present(self) -> int:
        return len(list(self.runs_folder.glob("run_*")))
