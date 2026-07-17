# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import numpy as np

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass

from ..effects import DeathEffect
from .node_module import NodeModule

if TYPE_CHECKING:
    from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HealthModule(NodeModule):
    """Age a node and retire it against a Gompertz-Makeham mortality hazard.

    Health is derived state, not independent state: it is recomputed from age
    every step as the node's hazard normalised against the hazard at max_age,
    giving a 0-100 frailty index. The death draw then reads that health, so
    the chain is hazard -> health -> chance of dying.

    Attributes:
        health: Current health on a 0-100 scale, recomputed from age.
        age: Current age, in the unit of the simulation's step size.
        baseline_hazard: Gompertz hazard at age 0.
        rate_of_aging: Rate at which the Gompertz hazard grows with age.
        ind_background_hazard: Age-independent (Makeham) hazard floor.
        max_age: Age at which health reaches 0 and death becomes certain.
    """

    name: ClassVar[str] = "health"

    health: float
    age: float
    baseline_hazard: float
    rate_of_aging: float
    ind_background_hazard: float
    max_age: float

    def apply(self, previous_state: SimulationState, rng: np.random.Generator) -> list:
        """Advance age one step, refresh health, and maybe emit a DeathEffect.

        Args:
            previous_state: The state being stepped from; only time_step is read.
            rng: Generator supplying the death draw.

        Returns:
            A single DeathEffect when the node dies, otherwise an empty list.
        """
        self.age += previous_state.time_step.factor
        self.health = health_from_hazard(
            self.age,
            self.baseline_hazard,
            self.rate_of_aging,
            self.ind_background_hazard,
            self.max_age,
        )

        if self._compute_death_chance(rng):
            return [DeathEffect(self.node_id)]
        return []

    def _compute_death_chance(self, rng: np.random.Generator) -> bool:
        # health is clamped to 0 past max_age, so this guard is belt-and-braces.
        if self.age > self.max_age:
            return True

        death_probability = 1 - self.health / 100
        to_die = rng.random() < death_probability
        return to_die


# ================================================================
# 2. Section: Functions — mortality hazard
# ================================================================
def gompertz_curve(x: float, baseline_hazard: float, rate_of_aging: float) -> float:
    """Gompertz hazard: mortality risk growing exponentially with age.

    Args:
        x: Age to evaluate the hazard at.
        baseline_hazard: Hazard at age 0.
        rate_of_aging: Exponential growth rate of the hazard.

    Returns:
        The age-dependent hazard at x.
    """
    return baseline_hazard * np.exp(rate_of_aging * x)


def hazard(
    x: float,
    baseline_hazard: float,
    rate_of_aging: float,
    ind_background_hazard: float,
) -> float:
    """Gompertz-Makeham hazard: the Gompertz curve over a constant floor.

    The floor is the age-independent risk (accidents and the like) that keeps
    even the youngest nodes from being immortal.

    Args:
        x: Age to evaluate the hazard at.
        baseline_hazard: Gompertz hazard at age 0.
        rate_of_aging: Exponential growth rate of the Gompertz hazard.
        ind_background_hazard: Age-independent hazard floor.

    Returns:
        The total hazard at x.
    """
    gompertz = gompertz_curve(x, baseline_hazard, rate_of_aging)
    return gompertz + ind_background_hazard


def health_from_hazard(
    x: float,
    baseline_hazard: float,
    rate_of_aging: float,
    ind_background_hazard: float,
    max_age: float,
) -> float:
    """Health as the hazard at x, normalised against the hazard at max_age.

    Approaches 100 where the hazard is negligible against the max_age hazard
    and hits 0 at (or past) max_age. Normalising this way means `1 - health /
    100` is exactly the hazard ratio, which is what the death draw uses.

    Args:
        x: Age to evaluate health at.
        baseline_hazard: Gompertz hazard at age 0.
        rate_of_aging: Exponential growth rate of the Gompertz hazard.
        ind_background_hazard: Age-independent hazard floor.
        max_age: Age at which health reaches 0.

    Returns:
        Health clamped to the 0-100 range.
    """
    mu = hazard(x, baseline_hazard, rate_of_aging, ind_background_hazard)
    mu_max = hazard(max_age, baseline_hazard, rate_of_aging, ind_background_hazard)
    return float(np.clip(100 * (1 - mu / mu_max), 0, 100))
