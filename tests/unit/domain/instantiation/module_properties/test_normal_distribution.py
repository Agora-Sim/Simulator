"""Contract tests for NormalDistribution.

NormalDistribution exposes the mean/std of its config dict and samples from a
Gaussian via random.normalvariate. Sampling is made deterministic in tests by
seeding the global random module.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import random
import statistics

import pytest

from simulator.domain.instantiation.module_properties.normal_distribution import (
    NormalDistribution,
)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_mean_and_std_read_from_data() -> None:
    dist = NormalDistribution(data={"type": "normal", "mean": 4.0, "std": 2.0})

    assert dist.mean == 4.0
    assert dist.std == 2.0


@pytest.mark.unit
def test_sample_returns_float() -> None:
    dist = NormalDistribution(data={"type": "normal", "mean": 0.0, "std": 1.0})

    assert isinstance(dist.sample(), float)


@pytest.mark.unit
def test_sample_is_reproducible_under_same_seed() -> None:
    dist = NormalDistribution(data={"type": "normal", "mean": 0.0, "std": 1.0})

    random.seed(123)
    first = dist.sample()
    random.seed(123)
    second = dist.sample()

    assert first == second


@pytest.mark.unit
def test_zero_std_always_samples_the_mean() -> None:
    dist = NormalDistribution(data={"type": "normal", "mean": 7.5, "std": 0.0})

    samples = [dist.sample() for _ in range(10)]

    assert all(sample == 7.5 for sample in samples)


@pytest.mark.unit
@pytest.mark.slow
def test_sample_distribution_is_approximately_gaussian() -> None:
    dist = NormalDistribution(data={"type": "normal", "mean": 100.0, "std": 5.0})

    random.seed(0)
    samples = [dist.sample() for _ in range(20_000)]

    assert statistics.fmean(samples) == pytest.approx(100.0, abs=0.2)
    assert statistics.pstdev(samples) == pytest.approx(5.0, abs=0.2)
