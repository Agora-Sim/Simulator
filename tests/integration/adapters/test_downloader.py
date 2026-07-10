"""Integration tests for Downloader.

Downloader serializes a Simulation to an HDF5 file under the run folder. These
tests exercise the real h5py write path through tmp_path (via the Source
fixture), checking the output location, return value, top-level structure and
input validation. Round-trip fidelity is covered separately in
test_downloader_loader_roundtrip.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import h5py
import pytest

from simulator.adapters.downloader import Downloader
from simulator.adapters.source import Source
from simulator.service.simulation_run import SimulationRun


# ================================================================
# 1. Section: Integration Tests
# ================================================================
@pytest.mark.integration
def test_download_run_writes_file_at_expected_path(
    source: Source, simulation: SimulationRun
) -> None:
    downloader = Downloader(source)

    out_path = downloader.download_run(simulation, run_nr=1)

    expected = source.get_run_folder("1") / "simulation.hdf5"
    assert out_path == expected
    assert out_path.exists()


@pytest.mark.integration
def test_download_run_creates_run_folder_when_missing(
    source: Source, simulation: SimulationRun
) -> None:
    assert not source.get_run_folder("1").exists()

    Downloader(source).download_run(simulation, run_nr=1)

    assert source.get_run_folder("1").is_dir()


@pytest.mark.integration
def test_download_run_writes_top_level_keys(
    source: Source, simulation: SimulationRun
) -> None:
    out_path = Downloader(source).download_run(simulation, run_nr=1)

    with h5py.File(out_path, "r") as f:
        assert set(f.keys()) == {"simulation_engine", "history", "current_step"}


@pytest.mark.integration
def test_download_run_returns_non_empty_file(
    source: Source, simulation: SimulationRun
) -> None:
    out_path = Downloader(source).download_run(simulation, run_nr=1)

    assert out_path.stat().st_size > 0


@pytest.mark.integration
def test_download_run_rejects_unsupported_file_type(
    source: Source, simulation: SimulationRun
) -> None:
    with pytest.raises(ValueError, match="Unsupported out_file_type"):
        Downloader(source).download_run(simulation, run_nr=1, out_file_type="json")
