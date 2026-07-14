"""Seed and random-event grounding tests.

Every random event in the simulator must draw from the single per-run NumPy
Generator that is threaded explicitly through the object graph, never from a
hidden global RNG. This suite pins that contract at three levels:

- Per random event: PercentageConnectivity.build and NormalDistribution.sample
  are reproducible under the same seed and untouched by the global RNG state.
- End to end: building and running a simulation with the same seed yields an
  identical population and connectivity; different seeds diverge.
- Between runs: the per-run streams derived from one master seed via
  SeedSequence.spawn are deterministic yet independent of each other.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import random
from dataclasses import asdict

import numpy as np
import pytest

from simulator.domain.instantiation.simulation_blueprint import SimulationBlueprint
from simulator.domain.instantiation.simulation_factory import SimulationFactory
from simulator.domain.instantiation.connectivity import PercentageConnectivity
from simulator.domain.instantiation.module_properties.normal_distribution import (
    NormalDistribution,
)
from tests.helpers.builders import (
    build_blueprint_data,
    build_percentage_connectivity_data,
)


# ================================================================
# 1. Section: Helpers
# ================================================================
def _spawn_run_rng(seed: int, run_index: int, nr_runs: int) -> np.random.Generator:
    """Per-run Generator, mirroring how the service run loop derives it."""
    children = np.random.SeedSequence(seed).spawn(nr_runs)
    return np.random.default_rng(children[run_index])


def _build_and_run(seed: int, run_index: int = 0, nr_runs: int = 1):
    """Build and run one simulation with a freshly derived per-run stream."""
    blueprint = SimulationBlueprint(build_blueprint_data())
    rng = _spawn_run_rng(seed, run_index, nr_runs)

    simulation = SimulationFactory().build_simulation(blueprint, rng)
    simulation.run_simulation(rng)
    return simulation


def _fingerprint(simulation) -> tuple:
    """A comparable snapshot of everything randomness should have decided."""
    matrix = simulation.engine.connectivity_matrix.data
    modules = [
        asdict(module) for node in simulation.engine.nodes for module in node.modules
    ]
    return matrix, modules


def _assert_same(first: tuple, second: tuple) -> None:
    np.testing.assert_array_equal(first[0], second[0])
    assert first[1] == second[1]


def _pollute_global_rngs(seed: int) -> None:
    """Advance both global RNGs so leakage would change grounded output."""
    np.random.seed(seed)
    random.seed(seed)


# ================================================================
# 2. Section: Per-Event — PercentageConnectivity
# ================================================================
@pytest.mark.unit
def test_connectivity_is_reproducible_under_same_seed() -> None:
    rule = PercentageConnectivity(build_percentage_connectivity_data(0.5))
    connection_dict = {"already_connected": [], "candidates": list(range(1, 20))}

    first = rule.build(0, connection_dict, np.random.default_rng(5))
    second = rule.build(0, connection_dict, np.random.default_rng(5))

    np.testing.assert_array_equal(first, second)


@pytest.mark.unit
def test_connectivity_ignores_global_rng_state() -> None:
    rule = PercentageConnectivity(build_percentage_connectivity_data(0.5))
    connection_dict = {"already_connected": [], "candidates": list(range(1, 20))}

    baseline = rule.build(0, connection_dict, np.random.default_rng(5))
    _pollute_global_rngs(999)
    after = rule.build(0, connection_dict, np.random.default_rng(5))

    np.testing.assert_array_equal(baseline, after)


@pytest.mark.unit
def test_connectivity_differs_under_different_seed() -> None:
    rule = PercentageConnectivity(build_percentage_connectivity_data(0.5))
    connection_dict = {"already_connected": [], "candidates": list(range(1, 20))}

    first = rule.build(0, connection_dict, np.random.default_rng(5))
    second = rule.build(0, connection_dict, np.random.default_rng(6))

    assert not np.array_equal(first, second)


# ================================================================
# 3. Section: Per-Event — NormalDistribution
# ================================================================
@pytest.mark.unit
def test_normal_sample_is_reproducible_under_same_seed() -> None:
    dist = NormalDistribution({"type": "normal", "mean": 0.0, "std": 1.0})

    assert dist.sample(np.random.default_rng(5)) == dist.sample(
        np.random.default_rng(5)
    )


@pytest.mark.unit
def test_normal_sample_ignores_global_rng_state() -> None:
    dist = NormalDistribution({"type": "normal", "mean": 0.0, "std": 1.0})

    baseline = dist.sample(np.random.default_rng(5))
    _pollute_global_rngs(999)
    after = dist.sample(np.random.default_rng(5))

    assert baseline == after


@pytest.mark.unit
def test_normal_sample_differs_under_different_seed() -> None:
    dist = NormalDistribution({"type": "normal", "mean": 0.0, "std": 1.0})

    assert dist.sample(np.random.default_rng(5)) != dist.sample(
        np.random.default_rng(6)
    )


# ================================================================
# 4. Section: End-to-End — a full build + run
# ================================================================
@pytest.mark.unit
def test_same_seed_reproduces_identical_simulation() -> None:
    first = _build_and_run(seed=42)
    second = _build_and_run(seed=42)

    _assert_same(_fingerprint(first), _fingerprint(second))


@pytest.mark.unit
def test_different_seed_produces_different_simulation() -> None:
    first = _fingerprint(_build_and_run(seed=42))
    second = _fingerprint(_build_and_run(seed=43))

    # Sampled module values are continuous, so they must diverge
    assert first[1] != second[1]


@pytest.mark.unit
def test_full_run_is_independent_of_global_rng_state() -> None:
    _pollute_global_rngs(111)
    first = _fingerprint(_build_and_run(seed=42))
    _pollute_global_rngs(222)
    second = _fingerprint(_build_and_run(seed=42))

    _assert_same(first, second)


# ================================================================
# 5. Section: Between-Runs — SeedSequence.spawn derivation
# ================================================================
@pytest.mark.unit
def test_spawned_run_streams_are_deterministic_from_master() -> None:
    first = _fingerprint(_build_and_run(seed=42, run_index=1, nr_runs=4))
    second = _fingerprint(_build_and_run(seed=42, run_index=1, nr_runs=4))

    _assert_same(first, second)


@pytest.mark.unit
def test_spawned_run_streams_are_independent_of_each_other() -> None:
    run_0 = _fingerprint(_build_and_run(seed=42, run_index=0, nr_runs=4))
    run_1 = _fingerprint(_build_and_run(seed=42, run_index=1, nr_runs=4))

    assert run_0[1] != run_1[1]


@pytest.mark.unit
def test_master_seed_change_shifts_every_run_stream() -> None:
    run_1_seed_a = _fingerprint(_build_and_run(seed=42, run_index=1, nr_runs=4))
    run_1_seed_b = _fingerprint(_build_and_run(seed=99, run_index=1, nr_runs=4))

    assert run_1_seed_a[1] != run_1_seed_b[1]
