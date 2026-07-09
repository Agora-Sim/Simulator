# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass

from simulator.adapters.source import Source
from simulator.adapters.simulation_io import SimulationIO


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Simulation:
    simulation_name: str
    simulation_description: str
    base_folder: Path = Path("data")

    @property
    def _source(self):
        return Source(
            simulation_name=self.simulation_name,
            simulation_description=self.simulation_description,
            base_folder=self.base_folder,
        )

    @property
    def _io(self):
        return SimulationIO(self._source)

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def init_simulation(self) -> Path:
        run_folder = self._io.init_simulation()
        return run_folder
