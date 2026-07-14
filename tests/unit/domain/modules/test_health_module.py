"""Contract tests for HealthModule.

HealthModule owns a node's ageing: apply() advances age by the step factor,
recomputes health from the decay curve and emits a DeathEffect when the death
draw fires. The death draw is pinned deterministically with stub generators:
random()=1.0 can never be below a probability <= 1 (never dies), random()=0.0
is below any positive probability (always dies).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest

from simulator.domain.effects import DeathEffect
from simulator.domain.modules import HealthModule
from simulator.domain.modules.health_module import decay_curve
from simulator.domain.simulation_state import SimulationState
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
    return HealthModule(health=50.0, age=age, decay_factor=100_000, max_age=100.0)


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_health_module_name_is_class_level() -> None:
    assert HealthModule.name == "health"


@pytest.mark.unit
def test_health_module_stores_fields() -> None:
    module = HealthModule(health=90.0, age=42.0, decay_factor=100_000, max_age=100.0)

    assert module.health == 90.0
    assert module.age == 42.0
    assert module.decay_factor == 100_000
    assert module.max_age == 100.0


# ──────────────────────────────────────────────────────
# 2.1 Subsection: apply()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_apply_advances_age_by_step_factor() -> None:
    module = _module(age=30.0)

    module.apply(_state(factor=0.5), _never_die_rng())

    assert module.age == 30.5


@pytest.mark.unit
def test_apply_recomputes_health_from_decay_curve() -> None:
    module = _module(age=30.0)

    module.apply(_state(factor=1.0), _never_die_rng())

    assert module.health == pytest.approx(decay_curve(31.0, 100_000, 100.0))


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
    # At max_age health is 0, so the death probability is 1 and even the
    # most favourable draw (just below 1) cannot save the node.
    module = _module(age=200.0)

    effects = module.apply(_state(), _luckiest_real_draw_rng())

    assert effects == [DeathEffect(node_id=module.node_id)]


# ──────────────────────────────────────────────────────
# 2.2 Subsection: decay_curve()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_decay_curve_is_full_health_at_age_zero() -> None:
    assert decay_curve(0.0, 100_000, 100.0) == pytest.approx(100.0)


@pytest.mark.unit
def test_decay_curve_is_zero_at_max_age() -> None:
    assert decay_curve(100.0, 100_000, 100.0) == pytest.approx(0.0)


@pytest.mark.unit
def test_decay_curve_clamps_past_max_age() -> None:
    assert decay_curve(150.0, 100_000, 100.0) == pytest.approx(0.0)


@pytest.mark.unit
def test_decay_curve_clamps_negative_age_to_full_health() -> None:
    assert decay_curve(-5.0, 100_000, 100.0) == pytest.approx(100.0)


@pytest.mark.unit
def test_decay_curve_decreases_with_age() -> None:
    young = decay_curve(30.0, 100_000, 100.0)
    old = decay_curve(60.0, 100_000, 100.0)

    assert young > old
