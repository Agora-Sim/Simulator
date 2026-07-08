"""Contract tests for NodeBlueprint.

NodeBlueprint is a view over the "nodes" config dict. It lists the node type
names, exposes a NodeProperty per type, and reports the total initial node count
(nr_nodes) as the sum of each type's initial_numbers.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.node_property import NodeProperty
from simulator.domain.instantiation.node_blueprint import NodeBlueprint
from tests.helpers.builders import (
    build_nodes_data,
    build_health_node_type_data,
    build_money_node_type_data,
)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_type_names_lists_every_node_type() -> None:
    blueprint = NodeBlueprint(build_nodes_data())

    assert blueprint.type_names == ["citizen", "company"]


@pytest.mark.unit
def test_node_properties_returns_one_property_per_type() -> None:
    blueprint = NodeBlueprint(build_nodes_data())

    props = blueprint.node_properties

    assert len(props) == 2
    assert all(isinstance(p, NodeProperty) for p in props)
    assert [p.name for p in props] == ["citizen", "company"]


@pytest.mark.unit
def test_nr_nodes_is_sum_of_initial_numbers() -> None:
    data = {
        "citizen": build_health_node_type_data(initial_numbers=3),
        "company": build_money_node_type_data(initial_numbers=2),
    }
    blueprint = NodeBlueprint(data)

    assert blueprint.nr_nodes == 5


@pytest.mark.unit
def test_nr_nodes_is_zero_for_empty_blueprint() -> None:
    blueprint = NodeBlueprint({})

    assert blueprint.nr_nodes == 0
    assert blueprint.type_names == []


@pytest.mark.unit
def test_get_node_type_properties_returns_named_property() -> None:
    blueprint = NodeBlueprint(build_nodes_data())

    prop = blueprint.get_node_type_properties("citizen")

    assert isinstance(prop, NodeProperty)
    assert prop.name == "citizen"
    assert prop.initial_numbers == 3


@pytest.mark.unit
def test_get_node_type_properties_unknown_type_raises_key_error() -> None:
    blueprint = NodeBlueprint(build_nodes_data())

    with pytest.raises(KeyError):
        blueprint.get_node_type_properties("does_not_exist")
