# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from abc import ABC

from .axis import Axis


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class BaseAggregator(ABC):
    name: str
    title: str
    plot_kind: str
    x: Axis
    y: Axis
