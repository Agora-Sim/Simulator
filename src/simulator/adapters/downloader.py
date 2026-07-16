# ================================================================
# 0. Section: IMPORTS
# ================================================================
import h5py
import numpy as np

from typing import Any
from pathlib import Path
from dataclasses import dataclass, is_dataclass, fields

from .source import Source
from ..domain.simulation_run import SimulationRun


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Downloader:
    source: Source

    def download_run(
        self, simulation: SimulationRun, run_nr: int, out_file_type: str = "hdf5"
    ) -> Path:
        if out_file_type != "hdf5":
            raise ValueError(f"Unsupported out_file_type: {out_file_type}")

        run_folder = self.source.get_run_folder(str(run_nr))
        run_folder.mkdir(parents=True, exist_ok=True)

        out_path = run_folder / f"simulation.{out_file_type}"

        with h5py.File(out_path, "w") as f:
            self._encode(f, "simulation_engine", simulation.engine)
            self._encode(f, "history", simulation.history)
            self._encode(f, "current_step", simulation.current_step)

        return out_path

    def _encode(self, group: h5py.Group, key: str, value: Any) -> None:
        if is_dataclass(value):
            sub = group.create_group(key)
            sub.attrs["__type__"] = type(value).__name__
            for f in fields(value):
                if not f.init:
                    continue
                self._encode(sub, f.name, getattr(value, f.name))

        elif isinstance(value, dict):
            sub = group.create_group(key)
            sub.attrs["__container__"] = "dict"
            for k, v in value.items():
                self._encode(sub, str(k), v)

        elif isinstance(value, (list, tuple)):
            sub = group.create_group(key)
            sub.attrs["__container__"] = "list"
            sub.attrs["__length__"] = len(value)
            for idx, item in enumerate(value):
                self._encode(sub, str(idx), item)

        elif value is None:
            sub = group.create_group(key)
            sub.attrs["__none__"] = True

        elif isinstance(value, np.ndarray):
            group.create_dataset(key, data=value)

        else:
            group.create_dataset(key, data=value)
