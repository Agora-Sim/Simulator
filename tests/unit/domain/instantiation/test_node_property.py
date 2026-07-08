"""Contract tests for NodeProperty.

NodeProperty is a view over a single node type's config. It exposes the initial
node count, the connectivity rule (dispatched by "type"), and the list of module
properties for the type.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.node_property import NodeProperty
from simulator.domain.instantiation.normal_connectivity import NormalConnectivity
from simulator.domain.instantiation.module_properties import ModuleProperty
from tests.helpers.builders import build_health_node_type_data


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_initial_numbers_reads_config() -> None:
    prop = NodeProperty(
        name="citizen", data=build_health_node_type_data(initial_numbers=42)
    )

    assert prop.initial_numbers == 42


@pytest.mark.unit
def test_connectivity_normal_type_returns_normal_connectivity() -> None:
    prop = NodeProperty(
        name="citizen", data=build_health_node_type_data(mean=2.0, std=1.0)
    )

    connectivity = prop.connectivity

    assert isinstance(connectivity, NormalConnectivity)
    assert connectivity.mean == 2.0
    assert connectivity.std == 1.0


@pytest.mark.unit
def test_connectivity_unknown_type_raises_value_error() -> None:
    data = build_health_node_type_data()
    data["connectivity"] = {"type": "wormhole"}
    prop = NodeProperty(name="citizen", data=data)

    with pytest.raises(ValueError, match="Unknown connectivity type: wormhole"):
        _ = prop.connectivity


@pytest.mark.unit
def test_modules_returns_one_module_property_per_module() -> None:
    prop = NodeProperty(name="citizen", data=build_health_node_type_data())

    modules = prop.modules

    assert len(modules) == 1
    assert all(isinstance(m, ModuleProperty) for m in modules)
    assert modules[0].name == "health_module"
