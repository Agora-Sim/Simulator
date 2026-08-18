# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

"""Unit tests for NodeColorMapper.

NodeColorMapper reduces a SimulationState to {node id: value} for the one
node type and module variable its NodeColorSpec names. Everything else is
skipped rather than defaulted: a different node type, a dead node, or a node
whose modules do not include the named one is simply absent from the result,
which is what lets the renderer grey those nodes out.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.node import Node
from simulator.domain.modules import MoneyModule
from simulator.domain.analysis import NodeColorMapper, NodeColorSpec

from tests.helpers.builders import build_health_module


# ================================================================
# 1. Section: Builders
# ================================================================
def _spec(**overrides) -> NodeColorSpec:
    """The canonical citizen/health/age spec, with per-test overrides."""
    return NodeColorSpec(
        **{
            "node_type": "citizen",
            "module_name": "health",
            "variable": "age",
            **overrides,
        }
    )


def _mapper(**overrides) -> NodeColorMapper:
    return NodeColorMapper(spec=_spec(**overrides))


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_values_reads_the_named_variable_for_each_matching_node(
    health_node, state_of
) -> None:
    state = state_of([health_node(0, age=30.0), health_node(1, age=41.5)])

    assert _mapper().values(state) == {0: 30.0, 1: 41.5}


@pytest.mark.unit
def test_values_returns_floats_not_the_raw_attribute(health_node, state_of) -> None:
    state = state_of([health_node(0, age=30)])

    assert isinstance(_mapper().values(state)[0], float)


@pytest.mark.unit
def test_values_skips_other_node_types(health_node, money_node, state_of) -> None:
    state = state_of([health_node(0), money_node(1)])

    assert set(_mapper().values(state)) == {0}


@pytest.mark.unit
def test_values_skips_dead_nodes(health_node, state_of) -> None:
    state = state_of([health_node(0, status=True), health_node(1, status=False)])

    assert set(_mapper().values(state)) == {0}


@pytest.mark.unit
def test_values_skips_nodes_without_the_named_module(state_of) -> None:
    # a citizen carrying the wrong module: matches on type, not on module
    node = Node(
        id=0,
        node_type="citizen",
        modules=[MoneyModule(balance=100.0, income=10.0)],
    )

    assert _mapper().values(state_of([node])) == {}


@pytest.mark.unit
def test_values_matches_the_module_by_its_classvar_name(state_of) -> None:
    node = Node(
        id=0,
        node_type="company",
        modules=[MoneyModule(balance=250.0, income=10.0)],
    )
    mapper = _mapper(node_type="company", module_name="money", variable="balance")

    assert mapper.values(state_of([node])) == {0: 250.0}


@pytest.mark.unit
def test_values_is_empty_when_nothing_matches(money_node, state_of) -> None:
    assert _mapper().values(state_of([money_node(0)])) == {}


@pytest.mark.unit
def test_values_keys_are_node_ids_not_positions(state_of) -> None:
    nodes = [
        Node(id=7, node_type="citizen", modules=[build_health_module(age=30.0)]),
        Node(id=3, node_type="citizen", modules=[build_health_module(age=40.0)]),
    ]

    assert _mapper().values(state_of(nodes)) == {7: 30.0, 3: 40.0}
