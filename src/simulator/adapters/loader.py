# ================================================================
# 0. Section: IMPORTS
# ================================================================
import h5py
import numpy as np

from typing import Any
from dataclasses import dataclass

from .source import Source
from ..service.simulation_run import SimulationRun
from ..domain import Node, ConnectivityMatrix, SimulationState, SimulationEngine
from ..domain.instantiation import SimulationSpecs
from ..domain.modules import Resource, HealthModule, MoneyModule, ResourcesModule

# ================================================================
# 1. Section: Registry
# ================================================================
_CLASS_REGISTRY: dict[str, type] = {
    cls.__name__: cls
    for cls in (
        SimulationEngine,
        Node,
        ConnectivityMatrix,
        SimulationState,
        SimulationSpecs,
        Resource,
        HealthModule,
        MoneyModule,
        ResourcesModule,
    )
}


# ================================================================
# 2. Section: Functions
# ================================================================
@dataclass
class Loader:
    source: Source

    def load_run(self, run_nr: int, out_file_type: str = "hdf5") -> SimulationRun:
        if out_file_type != "hdf5":
            raise ValueError(f"Unsupported out_file_type: {out_file_type}")

        run_folder = self.source.get_run_folder(str(run_nr))
        in_path = run_folder / f"simulation.{out_file_type}"

        with h5py.File(in_path, "r") as f:
            engine = self._decode(f["simulation_engine"])
            history = self._decode(f["history"])
            current_step = self._decode(f["current_step"])

        simulation = SimulationRun(engine=engine)
        simulation.current_step = current_step
        simulation.history = history

        return simulation

    def _decode(self, node: Any) -> Any:
        if isinstance(node, h5py.Dataset):
            return self._decode_dataset(node)

        if node.attrs.get("__none__"):
            return None

        container = node.attrs.get("__container__")
        if container == "list":
            return [self._decode(node[str(idx)]) for idx in range(len(node))]

        if container == "dict":
            return {key: self._decode(node[key]) for key in node.keys()}

        type_name = node.attrs.get("__type__")
        if type_name is not None:
            cls = _CLASS_REGISTRY[type_name]
            kwargs = {key: self._decode(node[key]) for key in node.keys()}
            return cls(**kwargs)

        raise ValueError(f"Cannot decode group: {node.name}")

    def _decode_dataset(self, dset: h5py.Dataset) -> Any:
        value = dset[()]

        if isinstance(value, np.ndarray):
            return value
        if isinstance(value, bytes):
            return value.decode()
        if isinstance(value, np.bool_):
            return bool(value)
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)

        return value
