"""Contract tests for Source.

Source is the path-logic value object shared by every adapter. It composes the
folder layout for a simulation (folder / runs_folder / config_path / run
folders) from a base_folder. It does not rename itself: simulation_name
disambiguation is Repository's responsibility (see
tests/integration/adapters/test_repository.py). These tests pin the path
composition, using tmp_path so nothing touches the real data/ tree.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

import pytest

from simulator.adapters.source import Source


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_source_folder_is_base_folder_joined_with_name(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.folder == tmp_path / "my_sim"


@pytest.mark.unit
def test_source_runs_folder_is_inside_simulation_folder(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.runs_folder == tmp_path / "my_sim" / "runs"


@pytest.mark.unit
def test_source_config_path_is_inside_simulation_folder(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.config_path == tmp_path / "my_sim" / "config.yaml"


@pytest.mark.unit
def test_source_get_run_folder_composes_run_directory(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.get_run_folder("3") == tmp_path / "my_sim" / "runs" / "run_3"


@pytest.mark.unit
def test_source_figures_folder_is_inside_simulation_folder(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.figures_folder == tmp_path / "my_sim" / "figures"


@pytest.mark.unit
def test_source_get_figure_path_composes_named_figure(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    expected = tmp_path / "my_sim" / "figures" / "health.png"
    assert source.get_figure_path("health", "png") == expected


@pytest.mark.unit
def test_source_get_nr_runs_present_is_zero_without_runs_folder(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.get_nr_runs_present() == 0


@pytest.mark.unit
def test_source_get_nr_runs_present_counts_only_run_directories(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)
    source.runs_folder.mkdir(parents=True)
    (source.runs_folder / "run_1").mkdir()
    (source.runs_folder / "run_2").mkdir()
    # Non-run entries must not be counted.
    (source.runs_folder / "notes.txt").touch()

    assert source.get_nr_runs_present() == 2


@pytest.mark.unit
def test_source_keeps_name_when_folder_does_not_exist(tmp_path: Path) -> None:
    source = Source("my_sim", "desc", base_folder=tmp_path)

    assert source.simulation_name == "my_sim"


@pytest.mark.unit
def test_source_keeps_name_even_when_folder_already_exists(tmp_path: Path) -> None:
    # Arrange: an existing folder for "my_sim".
    (tmp_path / "my_sim").mkdir()

    # Act
    source = Source("my_sim", "desc", base_folder=tmp_path)

    # Assert: Source itself never renames; that's Repository's job.
    assert source.simulation_name == "my_sim"
