"""Contract tests for the ModuleScalarMetric template.

ModuleScalarMetric factors out the shared per-node loop for scalar metrics:
given a `module` type and an `attribute` name, `calculate(state)` reads that
attribute off every living node carrying the module and returns their mean,
or 0.0 when no node qualifies. Concrete metrics only supply the ClassVars;
the base itself refuses to instantiate.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

import pytest

from simulator.domain.modules import HealthModule, NodeModule
from simulator.domain.analysis.metrics.module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Builders
# ================================================================
@dataclass
class _AgeProbe(ModuleScalarMetric):
    """Minimal concrete metric reading HealthModule.age via the template."""

    name: ClassVar[str] = "age_probe"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "age"
    title: ClassVar[str] = "Age Probe"


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_base_class_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        ModuleScalarMetric(unit="u")


@pytest.mark.unit
def test_subclass_without_config_cannot_be_instantiated() -> None:
    @dataclass
    class _Undeclared(ModuleScalarMetric):
        name: ClassVar[str] = "undeclared"
        title: ClassVar[str] = "Undeclared"

    with pytest.raises(TypeError):
        _Undeclared(unit="u")


@pytest.mark.unit
def test_calculate_averages_attribute_over_living_module_nodes(
    health_node, state_of
) -> None:
    state = state_of(
        [
            health_node(0, age=10.0),
            health_node(1, age=20.0),
            health_node(2, age=30.0),
        ]
    )

    assert _AgeProbe(unit="years").calculate(state) == 20.0


@pytest.mark.unit
def test_calculate_skips_dead_nodes(health_node, state_of) -> None:
    state = state_of(
        [
            health_node(0, age=10.0),
            health_node(1, age=90.0, status=False),
        ]
    )

    assert _AgeProbe(unit="years").calculate(state) == 10.0


@pytest.mark.unit
def test_calculate_skips_nodes_without_the_module(
    health_node, money_node, state_of
) -> None:
    state = state_of([health_node(0, age=40.0), money_node(1)])

    assert _AgeProbe(unit="years").calculate(state) == 40.0


@pytest.mark.unit
def test_calculate_returns_zero_when_no_node_qualifies(money_node, state_of) -> None:
    state = state_of([money_node(0), money_node(1)])

    assert _AgeProbe(unit="years").calculate(state) == 0.0
