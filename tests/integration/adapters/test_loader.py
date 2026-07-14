"""Integration tests for Loader.

Loader is the inverse of Downloader: it reads the HDF5 file for a run and
reconstructs a Simulation. These tests write a file with a real Downloader (both
adapters share the tmp_path Source) and check that Loader reconstructs concrete
domain types and coerces HDF5 scalars back to native Python types. Full
field-by-field fidelity lives in test_downloader_loader_roundtrip.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.adapters.downloader import Downloader
from simulator.adapters.loader import Loader
from simulator.adapters.source import Source
from simulator.domain import SimulationEngine, SimulationState
from simulator.domain.modules import HealthModule, MoneyModule
from simulator.service.simulation_run import SimulationRun


# ================================================================
# 1. Section: Integration Tests
# ================================================================
@pytest.mark.integration
def test_load_run_returns_simulation(source: Source, simulation: SimulationRun) -> None:
    Downloader(source).download_run(simulation, run_nr=1)

    loaded = Loader(source).load_run(run_nr=1)

    assert isinstance(loaded, SimulationRun)
    assert isinstance(loaded.engine, SimulationEngine)


@pytest.mark.integration
def test_load_run_reconstructs_concrete_module_types(
    source: Source, simulation: SimulationRun
) -> None:
    Downloader(source).download_run(simulation, run_nr=1)

    loaded = Loader(source).load_run(run_nr=1)

    modules = [module for node in loaded.engine.nodes for module in node.modules]
    assert any(isinstance(module, HealthModule) for module in modules)
    assert any(isinstance(module, MoneyModule) for module in modules)


@pytest.mark.integration
def test_load_run_reconstructs_history_states(
    source: Source, simulation: SimulationRun
) -> None:
    Downloader(source).download_run(simulation, run_nr=1)

    loaded = Loader(source).load_run(run_nr=1)

    assert len(loaded.history) == 1
    assert isinstance(loaded.history[0], SimulationState)


@pytest.mark.integration
def test_load_run_coerces_hdf5_scalars_to_native_types(
    source: Source, simulation: SimulationRun
) -> None:
    Downloader(source).download_run(simulation, run_nr=1)

    loaded = Loader(source).load_run(run_nr=1)

    specs = loaded.engine.simulation_specs.data
    # h5py hands back numpy scalars / bytes; the loader must coerce them back.
    assert isinstance(loaded.current_step, int)
    assert isinstance(specs["max_duration"], int)
    assert isinstance(specs["re_connection"], bool)
    assert isinstance(specs["step_size"], str)
    health_module = loaded.engine.nodes[0].modules[0]
    assert isinstance(health_module, HealthModule)
    assert isinstance(health_module.health, float)


@pytest.mark.integration
def test_load_run_rejects_unsupported_file_type(source: Source) -> None:
    with pytest.raises(ValueError, match="Unsupported out_file_type"):
        Loader(source).load_run(run_nr=1, out_file_type="json")
