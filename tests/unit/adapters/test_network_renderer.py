# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

"""Unit tests for NetworkRenderer.

NetworkRenderer turns a run history into an animated Plotly figure: an edge
trace and a node trace for the first state, plus one frame per later state
that swaps only the node trace. The contracts worth pinning are the ones a
reader cannot see from a screenshot — that the layout is computed once over
the union of every graph so nodes do not jump between frames, that the colour
range spans the whole history rather than each frame, that frame names line up
with the slider steps, and that unmapped nodes fall back to the neutral grey.
Plotly builds figures in memory, so nothing here touches the filesystem.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import cast

import numpy as np
import pytest
import plotly.graph_objects as go

from simulator.domain.node import Node
from simulator.domain.modules import MoneyModule
from simulator.domain.analysis import NodeColorMapper, NodeColorSpec
from simulator.adapters.render import NetworkRenderer

from tests.helpers.builders import (
    build_connectivity_matrix,
    build_engine,
    build_health_module,
)

SPEC = NodeColorSpec(node_type="citizen", module_name="health", variable="age")


# ================================================================
# 1. Section: Builders
# ================================================================
def _state(ages: list[float], time_idx: float, matrix: np.ndarray | None = None):
    """A state of citizens at the given ages, fully connected by default."""
    nodes = [
        Node(id=i, node_type="citizen", modules=[build_health_module(age=age)])
        for i, age in enumerate(ages)
    ]
    if matrix is None:
        matrix = 1.0 - np.eye(len(ages))

    state = build_engine(
        nodes=nodes,
        connectivity_matrix=build_connectivity_matrix(matrix),
    ).build_state()
    state.time_idx = time_idx
    return state


def _history() -> list:
    """Two steps of the same three citizens, ageing by one unit each step."""
    return [_state([30.0, 40.0, 50.0], 0.0), _state([31.0, 41.0, 51.0], 1.0)]


def _render(history: list | None = None, spec: NodeColorSpec = SPEC):
    if history is None:
        history = _history()
    return NetworkRenderer().render(history, spec, NodeColorMapper(spec=spec))


def _edge_trace(figure: go.Figure) -> go.Scatter:
    """The edge trace is the first entry in `data`.

    Plotly types `Figure.data` as a heterogeneous trace tuple, so the cast is
    what tells pyright which concrete trace these tests are reading.
    """
    return cast(go.Scatter, figure.data[0])


def _node_trace(figure: go.Figure) -> go.Scatter:
    """The node trace is the second entry in `data`; the first is the edges."""
    return cast(go.Scatter, figure.data[1])


def _frame_trace(figure: go.Figure, index: int) -> go.Scatter:
    """The single (node) trace each frame swaps in."""
    return cast(go.Scatter, figure.frames[index].data[0])


def _marker(trace: go.Scatter) -> go.scatter.Marker:
    """A trace's marker, which plotly types as an over-wide union."""
    return cast(go.scatter.Marker, trace.marker)


def _values(attribute) -> tuple:
    """A trace's x/y/text tuple, which plotly types as optional."""
    return cast(tuple, attribute)


# ================================================================
# 2. Section: Unit Tests
# ================================================================
@pytest.mark.unit
def test_render_puts_the_edge_trace_before_the_node_trace() -> None:
    figure = _render()

    assert _edge_trace(figure).mode == "lines"
    assert _node_trace(figure).mode == "markers"


@pytest.mark.unit
def test_render_emits_one_frame_per_state() -> None:
    figure = _render()

    assert len(figure.frames) == 2


@pytest.mark.unit
def test_frame_names_are_the_state_time_indices() -> None:
    figure = _render()

    assert [frame.name for frame in figure.frames] == ["0.0", "1.0"]


@pytest.mark.unit
def test_frames_target_the_node_trace_only() -> None:
    figure = _render()

    # plotly normalises the list it was given into a tuple
    assert all(tuple(frame.traces) == (1,) for frame in figure.frames)


@pytest.mark.unit
def test_slider_step_args_match_the_frame_names() -> None:
    figure = _render()

    steps = figure.layout.sliders[0].steps
    assert [step.args[0][0] for step in steps] == [f.name for f in figure.frames]


@pytest.mark.unit
def test_slider_has_one_step_per_state() -> None:
    figure = _render()

    assert len(figure.layout.sliders[0].steps) == 2


@pytest.mark.unit
def test_node_positions_are_shared_across_frames() -> None:
    figure = _render()

    first = _node_trace(figure)
    later = _frame_trace(figure, 1)
    assert _values(later.x) == _values(first.x)
    assert _values(later.y) == _values(first.y)


@pytest.mark.unit
def test_layout_covers_nodes_absent_from_the_first_state() -> None:
    # a node joining late must still get a position, or its frame would fail
    history = [_state([30.0], 0.0), _state([30.0, 40.0], 1.0)]

    figure = _render(history)

    assert len(_values(_frame_trace(figure, 1).x)) == 2


@pytest.mark.unit
def test_colour_range_spans_the_whole_history_not_one_frame() -> None:
    figure = _render()

    marker = _marker(_node_trace(figure))
    assert (marker.cmin, marker.cmax) == (30.0, 51.0)


@pytest.mark.unit
def test_colour_range_falls_back_when_nothing_is_mapped() -> None:
    spec = NodeColorSpec(node_type="ghost", module_name="health", variable="age")

    marker = _marker(_node_trace(_render(spec=spec)))
    assert (marker.cmin, marker.cmax) == (0.0, 1.0)


@pytest.mark.unit
def test_node_colours_are_the_mapped_values() -> None:
    figure = _render()

    assert _marker(_node_trace(figure)).color == (30.0, 40.0, 50.0)


@pytest.mark.unit
def test_unmapped_nodes_get_the_missing_colour_and_say_so_on_hover() -> None:
    nodes = [
        Node(id=0, node_type="citizen", modules=[build_health_module(age=30.0)]),
        Node(id=1, node_type="company", modules=[MoneyModule(balance=1.0, income=1.0)]),
    ]
    state = build_engine(
        nodes=nodes, connectivity_matrix=build_connectivity_matrix()
    ).build_state()

    trace = _node_trace(_render([state]))

    assert _marker(trace).color == (30.0, NetworkRenderer().missing_color)
    assert _values(trace.text)[1] == "node 1 no age"


@pytest.mark.unit
def test_hover_labels_report_the_variable_and_value() -> None:
    trace = _node_trace(_render())

    assert _values(trace.text)[0] == "node 0 age: 30.00"


@pytest.mark.unit
def test_edge_trace_separates_segments_with_none() -> None:
    matrix = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )

    edges = _edge_trace(_render([_state([30.0, 40.0, 50.0], 0.0, matrix)]))

    # two edges, each three entries long: start, end, then the None break
    xs = _values(edges.x)
    assert len(xs) == 6
    assert xs[2] is None and xs[5] is None


@pytest.mark.unit
def test_colorbar_and_colorscale_come_from_the_spec() -> None:
    spec = NodeColorSpec(
        node_type="citizen", module_name="health", variable="age", colormap="Plasma"
    )

    marker = _marker(_node_trace(_render(spec=spec)))
    assert _values(marker.colorscale)[0][1].lower().startswith("#")
    colorbar = cast(go.scatter.marker.ColorBar, marker.colorbar)
    assert colorbar.to_plotly_json()["title"]["text"] == "age"


@pytest.mark.unit
def test_render_is_reproducible_for_a_fixed_layout_seed() -> None:
    history = _history()

    first = _node_trace(NetworkRenderer(layout_seed=7).render(
        history, SPEC, NodeColorMapper(spec=SPEC)
    ))
    second = _node_trace(NetworkRenderer(layout_seed=7).render(
        history, SPEC, NodeColorMapper(spec=SPEC)
    ))

    assert _values(first.x) == _values(second.x)
    assert _values(first.y) == _values(second.y)


@pytest.mark.unit
def test_axes_are_hidden_and_equally_scaled() -> None:
    figure = _render()

    assert figure.layout.xaxis.visible is False
    assert figure.layout.yaxis.scaleanchor == "x"
