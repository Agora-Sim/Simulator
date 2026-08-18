# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import networkx as nx
import plotly.graph_objects as go

from dataclasses import dataclass, field

from ...domain import SimulationState
from ...domain.analysis import NodeColorMapper
from ...domain.analysis import NodeColorSpec
from .network_graph_builder import NetworkGraphBuilder


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NetworkRenderer:
    layout_seed: int = 42
    node_size: int = 16
    missing_color: str = "#c6ccd6"

    _builder: NetworkGraphBuilder = field(default_factory=NetworkGraphBuilder)

    def render(
        self,
        history: list[SimulationState],
        spec: NodeColorSpec,
        mapper: NodeColorMapper,
    ) -> go.Figure:
        graphs = [self._builder.build(state) for state in history]
        positions = self._layout(graphs)
        value_maps = [mapper.values(state) for state in history]
        cmin, cmax = self._value_range(value_maps)

        node_traces = [
            self._node_trace(graph, positions, values, spec, cmin, cmax)
            for graph, values in zip(graphs, value_maps)
        ]
        frames = [
            # 1. Traces=[1] targets the node trace's index in `data` below
            go.Frame(name=str(state.time_idx), data=[trace], traces=[1])
            for state, trace in zip(history, node_traces)
        ]

        figure = go.Figure(
            data=[self._edge_trace(graphs[0], positions), node_traces[0]],
            frames=frames,
        )
        # 2. Axes carry no meaning here: the layout coordinates are arbitrary
        figure.update_layout(
            sliders=[self._slider(history)],
            xaxis={"visible": False},
            yaxis={"visible": False, "scaleanchor": "x"},
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
        )
        return figure

    # ──────────────────────────────────────────────────────
    # 1.1 Subsection: Helper Functions
    # ──────────────────────────────────────────────────────
    def _layout(self, graphs: list[nx.Graph]) -> dict[int, tuple[float, float]]:
        union = nx.compose_all(graphs)
        # 1. Seed fixes the spring layout so re-exports are reproducible
        positions = nx.spring_layout(union, seed=self.layout_seed)
        # 2. Spring_layout hands back numpy arrays; plain tuples travel better
        return {int(i): (float(xy[0]), float(xy[1])) for i, xy in positions.items()}

    def _value_range(self, value_maps: list[dict[int, float]]) -> tuple[float, float]:
        values = [v for mapping in value_maps for v in mapping.values()]
        if not values:
            return 0.0, 1.0
        return min(values), max(values)

    # ──────────────────────────────────────────────────────
    # 1.2 Subsection: Traces
    # ──────────────────────────────────────────────────────
    def _edge_trace(self, graph: nx.Graph, positions: dict) -> go.Scatter:
        xs: list[float | None] = []
        ys: list[float | None] = []
        for source, target in graph.edges():
            x0, y0 = positions[source]
            x1, y1 = positions[target]
            # 1. The None breaks the line so segments do not join up
            xs.extend([x0, x1, None])
            ys.extend([y0, y1, None])

        return go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            line={"width": 0.6, "color": "#b0b7c3"},
            hoverinfo="skip",
            showlegend=False,
        )

    def _node_trace(
        self,
        graph: nx.Graph,
        positions: dict,
        values: dict[int, float],
        spec: NodeColorSpec,
        cmin: float,
        cmax: float,
    ) -> go.Scatter:
        ids = list(graph.nodes())
        # 1. Unmatched nodes get the neutral grey and say so on hover
        colors = [values.get(i, self.missing_color) for i in ids]
        labels = [
            (
                f"node {i} {spec.variable}: {values[i]:.2f}"
                if i in values
                else f"node {i} no {spec.variable}"
            )
            for i in ids
        ]

        return go.Scatter(
            x=[positions[i][0] for i in ids],
            y=[positions[i][1] for i in ids],
            mode="markers",
            marker={
                "size": self.node_size,
                "color": colors,
                "colorscale": spec.colormap,
                "cmin": cmin,
                "cmax": cmax,
                "showscale": True,
                "colorbar": {"title": spec.variable},
            },
            text=labels,
            hoverinfo="text",
            showlegend=False,
        )

    # ──────────────────────────────────────────────────────
    # 1.2 Subsection: Slider
    # ──────────────────────────────────────────────────────
    def _slider(self, history: list[SimulationState]) -> dict:
        steps = [
            {
                "label": f"{state.time_idx:g}",
                "method": "animate",
                # 1. Frame names must match go.Frame(name=...) exactly
                "args": [
                    [str(state.time_idx)],
                    {"mode": "immediate", "frame": {"redraw": True}},
                ],
            }
            for state in history
        ]
        return {"active": 0, "currentvalue": {"prefix": "t = "}, "steps": steps}
