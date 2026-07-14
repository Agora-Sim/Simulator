"""Integration tests for ConfigLoader.

ConfigLoader reads the YAML config at source.config_path and wraps its payload in
a SimulationBlueprint. These tests write a real YAML file under tmp_path and
check that the blueprint exposes the expected sub-views, and that a malformed
config surfaces through the blueprint's own validation.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import textwrap

import pytest
import yaml

from simulator.adapters.config_loader import ConfigLoader
from simulator.adapters.source import Source
from simulator.domain.instantiation import SimulationBlueprint
from tests.helpers import builders


# ================================================================
# 1. Section: Helpers
# ================================================================
def _write_config(source: Source, payload: dict) -> None:
    source.folder.mkdir(parents=True, exist_ok=True)
    with open(source.config_path, "w") as f:
        yaml.safe_dump(payload, f)


# ================================================================
# 2. Section: Integration Tests
# ================================================================
@pytest.mark.integration
def test_load_config_returns_blueprint(source: Source) -> None:
    _write_config(source, builders.build_blueprint_data())

    blueprint = ConfigLoader(source).load_config()

    assert isinstance(blueprint, SimulationBlueprint)


@pytest.mark.integration
def test_load_config_exposes_simulation_specs(source: Source) -> None:
    _write_config(source, builders.build_blueprint_data())

    blueprint = ConfigLoader(source).load_config()

    assert blueprint.simulation_specs.max_duration == 10
    assert blueprint.simulation_specs.seed == 42


@pytest.mark.integration
def test_load_config_exposes_node_blueprint(source: Source) -> None:
    _write_config(source, builders.build_blueprint_data())

    blueprint = ConfigLoader(source).load_config()

    # The canonical blueprint declares two node types: citizen and company.
    assert set(blueprint.node_blueprint.type_names) == {"citizen", "company"}


@pytest.mark.integration
def test_load_config_reads_yaml_written_on_disk(source: Source) -> None:
    source.folder.mkdir(parents=True, exist_ok=True)
    source.config_path.write_text(textwrap.dedent("""
            nodes:
              citizen:
                initial_numbers: 5
            simulation:
              max_duration: 99
              re_connection: false
              seed: 1
              step_size: 1 month
            """))

    blueprint = ConfigLoader(source).load_config()

    assert blueprint.simulation_specs.max_duration == 99


@pytest.mark.integration
def test_load_config_blueprint_rejects_missing_simulation_key(source: Source) -> None:
    _write_config(source, {"nodes": builders.build_nodes_data()})

    blueprint = ConfigLoader(source).load_config()

    with pytest.raises(ValueError, match="'simulation' key not found"):
        _ = blueprint.simulation_specs
