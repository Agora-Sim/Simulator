"""Integration tests for Repository.

Repository owns the on-disk lifecycle of a simulation: init_simulation
disambiguates the Source's simulation_name if a folder with that name already
exists, lays out the folder tree, and copies the default config (stamped with
the Source's name and description); init_run allocates the next sequentially
numbered run folder. These tests run against a tmp_path Source so nothing is
written into the real data/ tree. init_simulation reads the packaged default
config (src/simulator/adapters/configs/config.yaml) relative to the repo root.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest
import yaml

from simulator.adapters.repository import Repository
from simulator.adapters.source import Source


# ================================================================
# 1. Section: Integration Tests
# ================================================================
@pytest.mark.integration
def test_init_simulation_creates_folder_tree(source: Source) -> None:
    Repository(source).init_simulation()

    assert source.folder.is_dir()
    assert source.runs_folder.is_dir()


@pytest.mark.integration
def test_init_simulation_returns_simulation_folder(source: Source) -> None:
    result = Repository(source).init_simulation()

    assert result == source.folder


@pytest.mark.integration
def test_init_simulation_disambiguates_name_when_folder_already_exists(
    source: Source,
) -> None:
    # Arrange: an existing folder for the source's name containing two entries.
    existing = source.base_folder / source.simulation_name
    existing.mkdir()
    (existing / "runs").mkdir()
    (existing / "config.yaml").touch()

    # Act
    Repository(source).init_simulation()

    # Assert: name gets suffixed with the number of entries in the folder.
    assert source.simulation_name == "sim_2"


@pytest.mark.integration
def test_init_simulation_writes_config_stamped_with_source(source: Source) -> None:
    Repository(source).init_simulation()

    with open(source.config_path, "r") as f:
        config = yaml.safe_load(f)

    assert config["simulation_name"] == source.simulation_name
    assert config["simulation_description"] == source.simulation_description


@pytest.mark.integration
def test_init_run_creates_first_run_folder(source: Source) -> None:
    repository = Repository(source)
    repository.init_simulation()

    run_folder = repository.init_run()

    assert run_folder == source.get_run_folder("1")
    assert run_folder.is_dir()


@pytest.mark.integration
def test_init_run_increments_run_number(source: Source) -> None:
    repository = Repository(source)
    repository.init_simulation()

    first = repository.init_run()
    second = repository.init_run()

    assert first == source.get_run_folder("1")
    assert second == source.get_run_folder("2")
