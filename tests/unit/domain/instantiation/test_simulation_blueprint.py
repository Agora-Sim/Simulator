"""Contract tests for SimulationBlueprint.

SimulationBlueprint is the top-level view over the whole config dict. It exposes
a NodeBlueprint (from the "nodes" key) and a SimulationSpecs (from the
"simulation" key), raising a clear ValueError when either key is absent.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.instantiation.node_blueprint import NodeBlueprint
from simulator.domain.instantiation.simulation_specs import SimulationSpecs
from simulator.domain.instantiation.simulation_blueprint import SimulationBlueprint
from tests.helpers.builders import (
    build_blueprint_data,
    build_nodes_data,
    build_simulation_data,
)


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_node_blueprint_is_built_from_nodes_key() -> None:
    blueprint = SimulationBlueprint(build_blueprint_data())

    node_blueprint = blueprint.node_blueprint

    assert isinstance(node_blueprint, NodeBlueprint)
    assert node_blueprint.data == build_nodes_data()


@pytest.mark.unit
def test_simulation_specs_is_built_from_simulation_key() -> None:
    blueprint = SimulationBlueprint(build_blueprint_data())

    specs = blueprint.simulation_specs

    assert isinstance(specs, SimulationSpecs)
    assert specs.data == build_simulation_data()


@pytest.mark.unit
def test_node_blueprint_missing_nodes_key_raises_value_error() -> None:
    blueprint = SimulationBlueprint({"simulation": build_simulation_data()})

    with pytest.raises(ValueError, match="'nodes' key not found"):
        _ = blueprint.node_blueprint


@pytest.mark.unit
def test_simulation_specs_missing_simulation_key_raises_value_error() -> None:
    blueprint = SimulationBlueprint({"nodes": build_nodes_data()})

    with pytest.raises(ValueError, match="'simulation' key not found"):
        _ = blueprint.simulation_specs
