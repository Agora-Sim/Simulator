# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass

from simulator.domain.instantiation.simulation_blueprint import SimulationBlueprint
from simulator.domain.simulation_run import SimulationRun

from .source import Source
from .loader import Loader
from .repository import Repository
from .downloader import Downloader
from .config_loader import ConfigLoader


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SimulationIO:
    source: Source

    @property
    def _config_loader(self):
        return ConfigLoader(self.source)

    @property
    def _downloader(self):
        return Downloader(self.source)

    @property
    def _repository(self):
        return Repository(self.source)

    @property
    def _loader(self) -> Loader:
        return Loader(self.source)

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def init_simulation(self) -> Path:
        sim_folder = self._repository.init_simulation()

        return sim_folder

    def init_run(self) -> tuple[Path, int]:
        run_folder, run_id = self._repository.init_run()

        return run_folder, run_id

    def init_figures(self) -> Path:
        figures_folder = self._repository.init_figures()

        return figures_folder

    def load_config(self) -> SimulationBlueprint:
        blueprint = self._config_loader.load_config()
        return blueprint

    def download_run(
        self, simulation: SimulationRun, run_nr: int, out_file_type: str = "hdf5"
    ) -> Path:
        out_path = self._downloader.download_run(simulation, run_nr, out_file_type)
        return out_path

    def load_run(self, run_nr: int) -> SimulationRun:
        return self._loader.load_run(run_nr)

    def load_all_runs(self) -> list[SimulationRun]:
        return self._loader.load_all_runs()
