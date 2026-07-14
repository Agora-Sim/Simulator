# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re

import numpy as np

from tqdm import tqdm
from pathlib import Path
from dataclasses import dataclass

from ..adapters.source import Source
from .simulation_run import SimulationRun
from ..adapters.simulation_io import SimulationIO
from ..domain.instantiation.node_factory import NodeFactory
from ..domain.instantiation.simulation_factory import SimulationFactory


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

    @_source.setter
    def _source(self, value: Source):
        self.simulation_name = value.simulation_name
        self.simulation_description = value.simulation_description
        self.base_folder = value.base_folder

    @property
    def _io(self):
        return SimulationIO(self._source)

    @property
    def _node_factory(self):
        return NodeFactory()

    @property
    def _sim_factory(self):
        return SimulationFactory(self._node_factory)

    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def init_simulation(self) -> Path:
        self._source = _updated_simulation_name(self._source)
        self._io.source = self._source

        run_folder = SimulationIO(self._source).init_simulation()
        return run_folder

    def run_simulation(self) -> None:
        blueprint = self._io.load_config()

        nr_runs = blueprint.simulation_specs.nr_runs

        # Independent per-run streams derived from the master seed
        seed_sequence = np.random.SeedSequence(blueprint.simulation_specs.seed)
        run_seeds = seed_sequence.spawn(nr_runs)

        for run_idx in tqdm(range(nr_runs)):
            _, run_id = self._io.init_run()

            rng = np.random.default_rng(run_seeds[run_idx])
            simulation = self._sim_factory.build_simulation(blueprint, rng)
            simulation.run_simulation(rng)

            self._io.download_run(simulation, run_id)

    def load_run(self, run_nr: int) -> SimulationRun:
        return self._io.load_run(run_nr)


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def _updated_simulation_name(source: Source) -> Source:
    simulation_name = source.simulation_name

    if not source.base_folder.exists():
        return source

    pattern = re.compile(rf"{re.escape(simulation_name)}(_\d+)?$")
    nr_copies = len(
        [
            p
            for p in source.base_folder.iterdir()
            if p.is_dir() and pattern.fullmatch(p.name)
        ]
    )

    if nr_copies > 0:
        simulation_name = source.simulation_name + "_" + str(nr_copies + 1)

    source.simulation_name = simulation_name

    return source
