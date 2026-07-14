"""Contract tests for DeathEffect.

DeathEffect targets a single node by id and flips its status to False. It
must touch only that node, and applying it to an already-dead node must be
a harmless no-op (idempotence), since a node can plausibly receive several
death effects in one tick.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.effects import DeathEffect
from tests.helpers.builders import build_node, build_engine


# ================================================================
# 1. Section: Fixtures
# ================================================================
def _state_with_nodes(node_ids: list[int]):
    engine = build_engine(nodes=[build_node(node_id=i) for i in node_ids])
    return engine.build_state()


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_death_effect_name_and_priority_are_class_level() -> None:
    assert DeathEffect.name == "death"
    assert DeathEffect.priority == 0


@pytest.mark.unit
def test_apply_kills_the_targeted_node() -> None:
    state = _state_with_nodes([0, 1])

    DeathEffect(node_id=1).apply(state)

    assert state.nodes[1].status is False


@pytest.mark.unit
def test_apply_leaves_other_nodes_alive() -> None:
    state = _state_with_nodes([0, 1, 2])

    DeathEffect(node_id=1).apply(state)

    assert state.nodes[0].status is True
    assert state.nodes[2].status is True


@pytest.mark.unit
def test_apply_is_idempotent_on_a_dead_node() -> None:
    state = _state_with_nodes([0])

    DeathEffect(node_id=0).apply(state)
    DeathEffect(node_id=0).apply(state)

    assert state.nodes[0].status is False
