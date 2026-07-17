"""Contract tests for SimulationEngine.

SimulationEngine advances the population one step at a time in two phases:
it gathers effects from every module (all reading the same previous state),
then reduces them into the new state sorted by priority. Death is pinned
deterministically: a node past max_age has health clamped to 0, so its death
probability is 1 and any real rng draw kills it.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass, field

import numpy as np
import pytest

from simulator.domain.node import Node
from simulator.domain.effects import Effect
from simulator.domain.modules import HealthModule, MoneyModule
from simulator.domain.simulation_engine import SimulationEngine
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.instantiation.simulation_specs import SimulationSpecs
from tests.helpers.builders import (
    build_node,
    build_engine,
    build_health_module,
    build_simulation_data,
)

_RNG = np.random.default_rng(0)


# ================================================================
# 1. Section: Fixtures
# ================================================================
@dataclass
class _RecordingEffect(Effect):
    """Appends its label to a shared log so tests can assert apply order."""

    name: ClassVar[str] = "recording"
    priority: ClassVar[int] = 0

    label: str
    log: list = field(default_factory=list)

    def apply(self, state) -> None:
        self.log.append(self.label)


@dataclass
class _LateRecordingEffect(_RecordingEffect):
    name: ClassVar[str] = "late-recording"
    priority: ClassVar[int] = 10


def _elderly_citizen(node_id: int) -> Node:
    """A node past max_age: health clamps to 0, so death is guaranteed."""
    return build_node(
        node_id=node_id,
        modules=[build_health_module(health=0.0, age=200.0)],
    )


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_simulation_engine_stores_its_fields() -> None:
    nodes = [build_node(node_id=0)]
    connectivity = ConnectivityMatrix(data=np.zeros((1, 1)))
    specs = SimulationSpecs(build_simulation_data())

    engine = SimulationEngine(
        nodes=nodes,
        connectivity_matrix=connectivity,
        simulation_specs=specs,
    )

    assert engine.nodes == nodes
    assert engine.connectivity_matrix is connectivity
    assert engine.simulation_specs is specs


# ──────────────────────────────────────────────────────
# 2.1 Subsection: build_state()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_build_state_snapshots_engine_before_any_step() -> None:
    engine = build_engine()

    state = engine.build_state()

    # Snapshot holds equal values but independent objects (not aliased).
    assert state.nodes == engine.nodes
    assert state.nodes is not engine.nodes
    assert state.connectivity_matrix is not engine.connectivity_matrix
    assert state.time_idx == -1
    assert state.time_step == engine.simulation_specs.step_size


# ──────────────────────────────────────────────────────
# 2.2 Subsection: step()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_step_returns_state_stamped_with_current_step() -> None:
    engine = build_engine()

    state = engine.step(3.0, engine.build_state(), _RNG)

    assert state.time_idx == 3.0
    assert state.time_step == engine.simulation_specs.step_size


@pytest.mark.unit
def test_step_applies_death_effects_to_the_returned_state() -> None:
    engine = build_engine(nodes=[_elderly_citizen(0)])

    state = engine.step(0.0, engine.build_state(), _RNG)

    assert state.nodes[0].status is False


@pytest.mark.unit
def test_step_leaves_unaffected_nodes_alive() -> None:
    # A money-only node emits no effects and has no death draw, so it can
    # only die if someone else's effect wrongly targets it.
    bystander = build_node(
        node_id=1, node_type="company", modules=[MoneyModule(balance=1.0, income=1.0)]
    )
    engine = build_engine(nodes=[_elderly_citizen(0), bystander])

    state = engine.step(0.0, engine.build_state(), _RNG)

    assert state.nodes[0].status is False
    assert state.nodes[1].status is True


@pytest.mark.unit
def test_step_advances_module_state() -> None:
    engine = build_engine()
    health = engine.nodes[0].modules[0]
    assert isinstance(health, HealthModule)
    age_before = health.age

    engine.step(0.0, engine.build_state(), _RNG)

    assert health.age == age_before + engine.simulation_specs.step_size.factor


@pytest.mark.unit
def test_step_snapshots_are_not_aliased_across_history() -> None:
    # Regression: history entries must freeze per-step values; a shared
    # reference makes every state show the final age (a flat metric).
    engine = build_engine()
    factor = engine.simulation_specs.step_size.factor

    first = engine.step(0.0, engine.build_state(), _RNG)
    second = engine.step(1.0, first, _RNG)

    first_age = first.nodes[0].modules[0].age
    second_age = second.nodes[0].modules[0].age
    assert second_age == first_age + factor


# ──────────────────────────────────────────────────────
# 2.3 Subsection: reduce()
# ──────────────────────────────────────────────────────
@pytest.mark.unit
def test_reduce_applies_effects_in_priority_order() -> None:
    engine = build_engine()
    log: list[str] = []
    late = _LateRecordingEffect(label="late", log=log)
    early = _RecordingEffect(label="early", log=log)

    engine.reduce(engine.build_state(), [late, early])

    assert log == ["early", "late"]


@pytest.mark.unit
def test_reduce_preserves_insertion_order_for_equal_priorities() -> None:
    engine = build_engine()
    log: list[str] = []
    first = _RecordingEffect(label="first", log=log)
    second = _RecordingEffect(label="second", log=log)

    engine.reduce(engine.build_state(), [first, second])

    assert log == ["first", "second"]


@pytest.mark.unit
def test_reduce_with_no_effects_is_a_no_op() -> None:
    engine = build_engine()
    state = engine.build_state()

    engine.reduce(state, [])

    assert all(node.status is True for node in state.nodes)
