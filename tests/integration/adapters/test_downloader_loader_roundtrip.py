"""Round-trip integration tests for Downloader + Loader.

The two adapters are inverses: encoding a Simulation to HDF5 and decoding it back
must reconstruct an equivalent object graph. These tests are the contract that
keeps _encode and _decode in sync — if a new field or container type breaks the
symmetry, the field-by-field assertions here fail and point at it.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.adapters.downloader import Downloader
from simulator.adapters.loader import Loader
from simulator.adapters.source import Source
from simulator.domain.instantiation import SimulationSpecs
from simulator.domain.simulation_state import SimulationState
from tests.helpers import builders
from tests.helpers.assertions import assert_simulation_equal


# ================================================================
# 1. Section: Round-trip Tests
# ================================================================
@pytest.mark.integration
def test_roundtrip_preserves_full_simulation(source: Source) -> None:
    simulation = builders.build_simulation(current_step=1)

    Downloader(source).download_run(simulation, run_nr=1)
    loaded = Loader(source).load_run(run_nr=1)

    assert_simulation_equal(loaded, simulation)


@pytest.mark.integration
def test_roundtrip_preserves_connectivity_array(source: Source) -> None:
    matrix = np.array([[0.0, 0.5, 1.0], [1.0, 0.0, 0.5], [0.5, 1.0, 0.0]])
    engine = builders.build_engine(
        connectivity_matrix=builders.build_connectivity_matrix(matrix)
    )
    simulation = builders.build_simulation(engine=engine)

    Downloader(source).download_run(simulation, run_nr=1)
    loaded = Loader(source).load_run(run_nr=1)

    np.testing.assert_array_equal(loaded.engine.connectivity_matrix.data, matrix)


@pytest.mark.integration
def test_roundtrip_preserves_specs_dict(source: Source) -> None:
    specs = builders.build_simulation_specs(
        max_duration=12, re_connection=False, seed=7, step_size="2.5 days"
    )
    engine = builders.build_engine(simulation_specs=specs)
    simulation = builders.build_simulation(engine=engine)

    Downloader(source).download_run(simulation, run_nr=1)
    loaded = Loader(source).load_run(run_nr=1)

    assert isinstance(loaded.engine.simulation_specs, SimulationSpecs)
    assert loaded.engine.simulation_specs.data == specs.data


@pytest.mark.integration
def test_roundtrip_preserves_none_entries(source: Source) -> None:
    # None is a documented, supported leaf in the encoder; a None history slot
    # must survive the round-trip as None rather than an empty group.
    none_slot = cast(SimulationState, None)
    simulation = builders.build_simulation(history=[none_slot], current_step=1)

    Downloader(source).download_run(simulation, run_nr=1)
    loaded = Loader(source).load_run(run_nr=1)

    assert loaded.history == [None]


@pytest.mark.integration
def test_roundtrip_preserves_empty_history(source: Source) -> None:
    simulation = builders.build_simulation(history=[], current_step=0)

    Downloader(source).download_run(simulation, run_nr=1)
    loaded = Loader(source).load_run(run_nr=1)

    assert loaded.history == []
    assert loaded.current_step == 0
