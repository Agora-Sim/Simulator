"""Contract tests for the DistributionMetric template.

DistributionMetric factors out the shared per-node histogram loop for
distribution metrics: given a `module` type and an `attribute` name,
`calculate(state)` bins that attribute over living nodes carrying the module.
Concrete metrics only supply the ClassVars; the base itself refuses to
instantiate, same as ModuleScalarMetric.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass

import pytest

from simulator.domain.modules import HealthModule, NodeModule
from simulator.domain.analysis.metrics.distribution_metric import DistributionMetric


# ================================================================
# 1. Section: Builders
# ================================================================
@dataclass
class _AgeDistributionProbe(DistributionMetric):
    """Minimal concrete metric binning HealthModule.age via the template."""

    name: ClassVar[str] = "age_distribution_probe"
    module: ClassVar[type[NodeModule]] = HealthModule
    attribute: ClassVar[str] = "age"
    title: ClassVar[str] = "Age Distribution Probe"
    plot_kind: ClassVar[str] = "heatmap"


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_base_class_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match="module.*attribute"):
        DistributionMetric(unit="u")


@pytest.mark.unit
def test_subclass_without_config_cannot_be_instantiated() -> None:
    @dataclass
    class _Undeclared(DistributionMetric):
        name: ClassVar[str] = "undeclared"
        title: ClassVar[str] = "Undeclared"
        plot_kind: ClassVar[str] = "heatmap"

    with pytest.raises(TypeError, match="module.*attribute"):
        _Undeclared(unit="u")


@pytest.mark.unit
def test_declared_subclass_instantiates_fine() -> None:
    assert _AgeDistributionProbe(unit="years").nr_bins == 20
