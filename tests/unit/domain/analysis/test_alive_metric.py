"""Contract tests for AliveMetric.

AliveMetric reads node status rather than a module attribute, so it extends
Metric directly and counts dead nodes instead of skipping them.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pytest

from simulator.domain.analysis.metrics import AliveMetric, Metric
from simulator.domain.analysis.metrics.module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_alive_metric_config_is_class_level() -> None:
    assert issubclass(AliveMetric, Metric)
    assert not issubclass(AliveMetric, ModuleScalarMetric)
    assert AliveMetric.name == "alive_metric"
    assert AliveMetric.title == "Alive Metric"


@pytest.mark.unit
def test_unit_defaults_to_percent() -> None:
    assert AliveMetric().unit == "%"


@pytest.mark.unit
def test_calculate_returns_percentage_of_living_nodes(health_node, state_of) -> None:
    state = state_of(
        [
            health_node(0),
            health_node(1),
            health_node(2, status=False),
            health_node(3, status=False),
        ]
    )

    assert AliveMetric().calculate(state) == 50.0


@pytest.mark.unit
def test_calculate_counts_nodes_without_a_health_module(
    health_node, money_node, state_of
) -> None:
    state = state_of([health_node(0), money_node(1)])

    assert AliveMetric().calculate(state) == 100.0


@pytest.mark.unit
def test_calculate_returns_zero_on_empty_population(state_of) -> None:
    assert AliveMetric().calculate(state_of([])) == 0.0
