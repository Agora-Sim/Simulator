"""Contract tests for HealthModule.

HealthModule owns a node's ageing: apply() advances age by the step factor,
recomputes health from the Gompertz-Makeham hazard and emits a DeathEffect
when the death draw fires. The death draw is pinned deterministically with
stub generators: random()=1.0 can never be below a probability <= 1 (never
dies), random()=0.0 is below any positive probability (always dies).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.effects import DeathEffect
from simulator.domain.modules import HealthModule
from simulator.domain.modules.health_module import (
    gompertz_curve,
    hazard,
    health_from_hazard,
)
from simulator.domain.simulation_state import SimulationState
from tests.helpers.builders import HEALTH_PARAMS, build_health_module
from tests.helpers.fakes import FakeStepType


# ================================================================
# 1. Section: Fixtures
# ================================================================
class _FakeState:
    """Minimal previous_state stand-in: apply() only reads time_step.factor."""

    def __init__(self, factor: float = 1.0) -> None:
        self.time_step = FakeStepType(factor=factor)


class _FixedRng:
    """Stub generator returning a fixed draw, for deterministic death tests."""

    def __init__(self, draw: float) -> None:
        self._draw = draw

    def random(self) -> float:
        return self._draw


def _state(factor: float = 1.0) -> SimulationState:
    return cast(SimulationState, _FakeState(factor))


def _never_die_rng() -> np.random.Generator:
    return cast(np.random.Generator, _FixedRng(1.0))


def _always_die_rng() -> np.random.Generator:
    return cast(np.random.Generator, _FixedRng(0.0))


def _luckiest_real_draw_rng() -> np.random.Generator:
    # The best draw a real generator can produce: random() is always < 1.
    return cast(np.random.Generator, _FixedRng(0.999_999_999))


def _module(age: float = 30.0) -> HealthModule:
    return build_health_module(health=50.0, age=age)


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_health_module_name_is_class_level() -> None:
    assert HealthModule.name == "health"


@pytest.mark.unit
def test_health_module_stores_fields() -> None:
    module = build_health_module(health=90.0, age=42.0)

    assert module.health == 90.0
    assert module.age == 42.0
    assert module.baseline_hazard == HEALTH_PARAMS["baseline_hazard"]
    assert module.rate_of_aging == HEALTH_PARAMS["rate_of_aging"]
    assert module.ind_background_hazard == HEALTH_PARAMS["ind_background_hazard"]
    assert module.max_age == HEALTH_PARAMS["max_age"]


# ──────────────────────────────────────────────────────
# 2.1 Subsection: apply()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_apply_advances_age_by_step_factor() -> None:
    module = _module(age=30.0)

    module.apply(_state(factor=0.5), _never_die_rng())

    assert module.age == 30.5


@pytest.mark.unit
def test_apply_recomputes_health_from_the_hazard() -> None:
    module = _module(age=30.0)

    module.apply(_state(factor=1.0), _never_die_rng())

    assert module.health == pytest.approx(health_from_hazard(31.0, **HEALTH_PARAMS))


@pytest.mark.unit
def test_apply_overwrites_the_seeded_health() -> None:
    # health is derived from age, so the configured value cannot survive a step.
    module = build_health_module(health=50.0, age=30.0)

    module.apply(_state(), _never_die_rng())

    assert module.health != 50.0


@pytest.mark.unit
def test_apply_returns_no_effects_when_the_node_survives() -> None:
    module = _module(age=30.0)

    effects = module.apply(_state(), _never_die_rng())

    assert effects == []


@pytest.mark.unit
def test_apply_returns_death_effect_carrying_the_node_id() -> None:
    module = _module(age=30.0)
    module.node_id = 7

    effects = module.apply(_state(), _always_die_rng())

    assert effects == [DeathEffect(node_id=7)]


@pytest.mark.unit
def test_node_past_max_age_always_emits_death_effect() -> None:
    # Past max_age health clamps to 0, so the death probability is 1 and even
    # the most favourable draw (just below 1) cannot save the node.
    module = _module(age=200.0)

    effects = module.apply(_state(), _luckiest_real_draw_rng())

    assert effects == [DeathEffect(node_id=module.node_id)]


@pytest.mark.unit
def test_health_decreases_as_the_node_ages() -> None:
    module = _module(age=30.0)

    module.apply(_state(factor=10.0), _never_die_rng())
    younger = module.health
    module.apply(_state(factor=10.0), _never_die_rng())

    assert module.health < younger


# ──────────────────────────────────────────────────────
# 2.2 Subsection: the hazard model
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_gompertz_curve_is_the_baseline_hazard_at_age_zero() -> None:
    assert gompertz_curve(0.0, 8.0e-6, 0.08) == pytest.approx(8.0e-6)


@pytest.mark.unit
def test_gompertz_curve_grows_exponentially_with_age() -> None:
    # A fixed age gap multiplies the hazard by the same factor wherever it sits.
    ratio_low = gompertz_curve(10.0, 8.0e-6, 0.08) / gompertz_curve(0.0, 8.0e-6, 0.08)
    ratio_high = gompertz_curve(60.0, 8.0e-6, 0.08) / gompertz_curve(50.0, 8.0e-6, 0.08)

    assert ratio_low == pytest.approx(ratio_high)


@pytest.mark.unit
def test_hazard_adds_the_age_independent_floor() -> None:
    gompertz = gompertz_curve(30.0, 8.0e-6, 0.08)

    assert hazard(30.0, 8.0e-6, 0.08, 6.0e-5) == pytest.approx(gompertz + 6.0e-5)


@pytest.mark.unit
def test_hazard_is_never_below_the_floor() -> None:
    assert hazard(0.0, 8.0e-6, 0.08, 6.0e-5) > 6.0e-5


@pytest.mark.unit
def test_health_from_hazard_is_near_full_at_age_zero() -> None:
    # Not exactly 100: the age-0 hazard is small against max_age, not absent.
    assert health_from_hazard(0.0, **HEALTH_PARAMS) > 99.0


@pytest.mark.unit
def test_health_from_hazard_is_zero_at_max_age() -> None:
    assert health_from_hazard(100.0, **HEALTH_PARAMS) == pytest.approx(0.0)


@pytest.mark.unit
def test_health_from_hazard_clamps_past_max_age() -> None:
    assert health_from_hazard(150.0, **HEALTH_PARAMS) == pytest.approx(0.0)


@pytest.mark.unit
def test_health_from_hazard_decreases_with_age() -> None:
    young = health_from_hazard(30.0, **HEALTH_PARAMS)
    old = health_from_hazard(60.0, **HEALTH_PARAMS)

    assert young > old


@pytest.mark.unit
def test_death_probability_is_the_normalised_hazard_ratio() -> None:
    # health is defined so that 1 - health/100 is exactly the hazard ratio the
    # death draw compares against; this pins that identity.
    age = 70.0
    health = health_from_hazard(age, **HEALTH_PARAMS)
    mu = hazard(
        age,
        HEALTH_PARAMS["baseline_hazard"],
        HEALTH_PARAMS["rate_of_aging"],
        HEALTH_PARAMS["ind_background_hazard"],
    )
    mu_max = hazard(
        HEALTH_PARAMS["max_age"],
        HEALTH_PARAMS["baseline_hazard"],
        HEALTH_PARAMS["rate_of_aging"],
        HEALTH_PARAMS["ind_background_hazard"],
    )

    assert 1 - health / 100 == pytest.approx(mu / mu_max)
