# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import plotly.graph_objects as go

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
        figures_path = self.source.figures_folder

        for fmt in formats:
            figure.savefig(figures_path / f"{name}.{fmt}", format=fmt)
        return [figures_path / f"{name}.{fmt}" for fmt in formats]

    def export_graph_interactive(self, figure: go.Figure, name: str) -> Path:
        path = self.source.get_figure_path(name, "html")
        figure.write_html(path, include_plotlyjs="inline", full_html=True)
        return path
