# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass
from matplotlib.figure import Figure

from ..source import Source



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class FigureExporter:
    source: Source

    def export(self, figure: Figure, name: str, formats: list[str]) -> list[Path]:
        pass
