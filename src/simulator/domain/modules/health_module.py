# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import numpy as np

from typing import ClassVar, TYPE_CHECKING
from dataclasses import dataclass

from ..effects import Effect, DeathEffect
from .node_module import NodeModule

if TYPE_CHECKING:
    from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class HealthModule(NodeModule):
    name: ClassVar[str] = "health"

    health: float
    age: float
    decay_factor: float
    max_age: float

    def apply(self, previous_state: SimulationState, rng: np.random.Generator) -> list:
        self.age += previous_state.time_step.factor
        self.health = decay_curve(self.age, self.decay_factor, self.max_age)

        if self._compute_death_chance(rng):
            return [DeathEffect(self.node_id)]
        return []

    def _compute_death_chance(self, rng: np.random.Generator) -> bool:
        death_probability = 1 - self.health / 100
        to_die = rng.random() < death_probability
        return to_die


def decay_curve(x: float, decay_factor: float, max_age: float) -> float:
    c = decay_factor
    x = np.clip(x, 0, max_age)
    return 100 * np.log(1 + c * (1 - x / max_age)) / np.log(1 + c)
