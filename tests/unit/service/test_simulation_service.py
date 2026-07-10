"""Contract tests for the Simulation service.

Simulation is a thin facade over a Source and a SimulationIO. Its one job in
init_simulation is to resolve a non-colliding simulation_name (appending a
copy suffix when a folder with that name already exists) and then hand the
*updated* Source to SimulationIO to do the real filesystem work.

The regression these tests guard: because _source/_io are properties that
rebuild a fresh Source on every access, the name update must be written back
onto the service so the SimulationIO that runs actually sees the new name.
SimulationIO is monkeypatched with a recording fake so these stay filesystem
free — the real I/O is covered by the adapter integration tests.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

import pytest

from simulator.service import simulation as simulation_module
from simulator.service.simulation import Simulation, _updated_simulation_name
from simulator.adapters.source import Source


# ================================================================
# 1. Section: Fakes
# ================================================================
class RecordingSimulationIO:
    """Records the Source it was constructed with and the run folder to return."""

    instances: list["RecordingSimulationIO"] = []

    def __init__(self, source: Source) -> None:
        # Snapshot the name at construction time: the service mutates the same
        # Source object, so we must capture the value the IO would actually use.
        self.source = source
        self.name_at_construction = source.simulation_name
        self.init_simulation_calls = 0
        RecordingSimulationIO.instances.append(self)

    def init_simulation(self) -> Path:
        self.init_simulation_calls += 1
        return Path("data") / self.source.simulation_name


@pytest.fixture(autouse=True)
def _reset_io_instances() -> None:
    RecordingSimulationIO.instances = []


@pytest.fixture
def patched_io(monkeypatch: pytest.MonkeyPatch) -> type[RecordingSimulationIO]:
    monkeypatch.setattr(simulation_module, "SimulationIO", RecordingSimulationIO)
    return RecordingSimulationIO


# ================================================================
# 2. Section: Fixtures
# ================================================================
def _make_simulation(base_folder: Path, name: str = "sim") -> Simulation:
    return Simulation(
        simulation_name=name,
        simulation_description="desc",
        base_folder=base_folder,
    )


# ================================================================
# 3. Section: Unit Tests — init_simulation
# ================================================================
@pytest.mark.unit
def test_init_simulation_keeps_name_when_no_existing_folder(
    tmp_path: Path, patched_io: type[RecordingSimulationIO]
) -> None:
    simulation = _make_simulation(tmp_path)

    simulation.init_simulation()

    assert patched_io.instances[-1].name_at_construction == "sim"


@pytest.mark.unit
def test_init_simulation_appends_suffix_when_name_already_exists(
    tmp_path: Path, patched_io: type[RecordingSimulationIO]
) -> None:
    (tmp_path / "sim").mkdir()
    simulation = _make_simulation(tmp_path)

    simulation.init_simulation()

    assert patched_io.instances[-1].name_at_construction == "sim_2"


@pytest.mark.unit
def test_init_simulation_counts_all_existing_copies(
    tmp_path: Path, patched_io: type[RecordingSimulationIO]
) -> None:
    (tmp_path / "sim").mkdir()
    (tmp_path / "sim_2").mkdir()
    simulation = _make_simulation(tmp_path)

    simulation.init_simulation()

    assert patched_io.instances[-1].name_at_construction == "sim_3"


@pytest.mark.unit
def test_init_simulation_writes_updated_name_back_onto_service(
    tmp_path: Path, patched_io: type[RecordingSimulationIO]
) -> None:
    # Regression: the property rebuilds Source on each access, so the updated
    # name must be persisted on the service, not lost on the throwaway Source.
    (tmp_path / "sim").mkdir()
    simulation = _make_simulation(tmp_path)

    simulation.init_simulation()

    assert simulation.simulation_name == "sim_2"


@pytest.mark.unit
def test_init_simulation_returns_run_folder_from_io(
    tmp_path: Path, patched_io: type[RecordingSimulationIO]
) -> None:
    simulation = _make_simulation(tmp_path)

    run_folder = simulation.init_simulation()

    io = patched_io.instances[-1]
    assert io.init_simulation_calls == 1
    assert run_folder == Path("data") / "sim"


# ================================================================
# 4. Section: Unit Tests — _updated_simulation_name helper
# ================================================================
@pytest.mark.unit
def test_updated_simulation_name_unchanged_without_existing_copies(
    tmp_path: Path,
) -> None:
    source = Source("sim", "desc", base_folder=tmp_path)

    result = _updated_simulation_name(source)

    assert result.simulation_name == "sim"
    assert result is source


@pytest.mark.unit
def test_updated_simulation_name_appends_next_index(tmp_path: Path) -> None:
    (tmp_path / "sim").mkdir()
    source = Source("sim", "desc", base_folder=tmp_path)

    result = _updated_simulation_name(source)

    assert result.simulation_name == "sim_2"


@pytest.mark.unit
def test_updated_simulation_name_ignores_prefix_only_matches(tmp_path: Path) -> None:
    # "simulation" shares a prefix with "sim" but is a different simulation.
    (tmp_path / "simulation").mkdir()
    (tmp_path / "sim_backup").mkdir()
    source = Source("sim", "desc", base_folder=tmp_path)

    result = _updated_simulation_name(source)

    assert result.simulation_name == "sim"


@pytest.mark.unit
def test_updated_simulation_name_ignores_files(tmp_path: Path) -> None:
    # A stray file named like the simulation must not count as a copy.
    (tmp_path / "sim").touch()
    source = Source("sim", "desc", base_folder=tmp_path)

    result = _updated_simulation_name(source)

    assert result.simulation_name == "sim"


@pytest.mark.unit
def test_updated_simulation_name_handles_missing_base_folder(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist"
    source = Source("sim", "desc", base_folder=missing)

    result = _updated_simulation_name(source)

    assert result.simulation_name == "sim"
