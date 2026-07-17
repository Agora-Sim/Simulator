"""Contract tests for AgeMetric.

AgeMetric is config-only over ModuleScalarMetric: it reads HealthModule.age
and averages it across living nodes. Its identity (name, module, attribute,
title, plot_kind) lives in ClassVars; `unit` is the sole instance field and
has no default, so a unit must be supplied at construction.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import dataclasses

import pytest

from simulator.domain.modules import HealthModule
from simulator.domain.analysis.metrics import AgeMetric, Metric
from simulator.domain.analysis.metrics.module_scalar_metric import ModuleScalarMetric


# ================================================================
# 1. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_age_metric_config_is_class_level() -> None:
    assert issubclass(AgeMetric, (ModuleScalarMetric, Metric))
    assert AgeMetric.name == "age_metric"
    assert AgeMetric.title == "Age Metric"
    assert AgeMetric.module is HealthModule
    assert AgeMetric.attribute == "age"
    assert AgeMetric.plot_kind == "line"


@pytest.mark.unit
def test_unit_is_the_only_instance_field() -> None:
    assert [f.name for f in dataclasses.fields(AgeMetric)] == ["unit"]
    assert AgeMetric(unit="years").unit == "years"


@pytest.mark.unit
def test_calculate_averages_age_over_living_nodes(health_node, state_of) -> None:
    state = state_of(
        [
            health_node(0, age=10.0),
            health_node(1, age=50.0),
            health_node(2, age=90.0, status=False),
        ]
    )

    assert AgeMetric(unit="years").calculate(state) == 30.0


@pytest.mark.unit
def test_calculate_returns_zero_on_empty_population(state_of) -> None:
    assert AgeMetric(unit="years").calculate(state_of([])) == 0.0
