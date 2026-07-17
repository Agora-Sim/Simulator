"""Contract tests for HealthMetric.

HealthMetric mirrors AgeMetric but reads HealthModule.health and defaults its
`unit` to "%", so it constructs with no arguments.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.modules import HealthModule
from simulator.domain.analysis.metrics import HealthMetric, Metric
from simulator.domain.analysis.metrics.module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_health_metric_config_is_class_level() -> None:
    assert issubclass(HealthMetric, (ModuleScalarMetric, Metric))
    assert HealthMetric.name == "health_metric"
    assert HealthMetric.title == "Health Metric"
    assert HealthMetric.module is HealthModule
    assert HealthMetric.attribute == "health"
    assert HealthMetric.plot_kind == "line"


@pytest.mark.unit
def test_unit_defaults_to_percent() -> None:
    assert HealthMetric().unit == "%"


@pytest.mark.unit
def test_calculate_averages_health_over_living_nodes(health_node, state_of) -> None:
    state = state_of(
        [
            health_node(0, health=40.0),
            health_node(1, health=60.0),
            health_node(2, health=0.0, status=False),
        ]
    )

    assert HealthMetric().calculate(state) == 50.0


@pytest.mark.unit
def test_calculate_returns_zero_on_empty_population(state_of) -> None:
    assert HealthMetric().calculate(state_of([])) == 0.0
