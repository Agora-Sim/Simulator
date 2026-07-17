"""Builders for domain test data.

These helpers produce the raw config dictionaries the domain instantiation
layer consumes, plus convenience builders for concrete domain objects. Keeping
the canonical shapes in one place means a change to the config schema only has
to be reflected here, not in every test.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from simulator.domain.node import Node
from simulator.domain.connectivity_matrix import ConnectivityMatrix
from simulator.domain.simulation_state import SimulationState
from simulator.domain.simulation_engine import SimulationEngine
from simulator.domain.instantiation import SimulationSpecs
from simulator.domain.modules import HealthModule, MoneyModule
from simulator.domain.simulation_run import SimulationRun

# Canonical Gompertz-Makeham parameters, on a years scale (max_age 100), so
# tests keep the readable ages they had before the hazard model landed.
HEALTH_PARAMS: dict[str, float] = {
    "baseline_hazard": 8.0e-6,
    "rate_of_aging": 0.08,
    "ind_background_hazard": 6.0e-5,
    "max_age": 100.0,
}


# ──────────────────────────────────────────────────────
# Raw config-dict builders (what the user file would contain)
# ──────────────────────────────────────────────────────
def build_percentage_connectivity_data(percentage: float = 0.5) -> dict[str, Any]:
    return {"type": "percentage", "percentage": percentage}


def build_variable_data(
    range_min: float = 0.0,
    range_max: float = 100.0,
    mean: float = 50.0,
    std: float = 5.0,
) -> dict[str, Any]:
    return {
        "range": [range_min, range_max],
        "distribution": {"type": "normal", "mean": mean, "std": std},
    }


def build_health_node_type_data(
    initial_numbers: int = 3, percentage: float = 0.5
) -> dict[str, Any]:
    return {
        "initial_numbers": initial_numbers,
        "connectivity": build_percentage_connectivity_data(percentage=percentage),
        "modules": {
            "health": {
                "health": build_variable_data(mean=50.0, std=5.0),
                "age": build_variable_data(mean=30.0, std=2.0),
                "baseline_hazard": build_variable_data(
                    mean=HEALTH_PARAMS["baseline_hazard"], std=0.0
                ),
                "rate_of_aging": build_variable_data(
                    mean=HEALTH_PARAMS["rate_of_aging"], std=0.0
                ),
                "ind_background_hazard": build_variable_data(
                    mean=HEALTH_PARAMS["ind_background_hazard"], std=0.0
                ),
                "max_age": build_variable_data(mean=HEALTH_PARAMS["max_age"], std=0.0),
            }
        },
    }


def build_money_node_type_data(initial_numbers: int = 2) -> dict[str, Any]:
    return {
        "initial_numbers": initial_numbers,
        "connectivity": build_percentage_connectivity_data(percentage=0.5),
        "modules": {
            "money": {
                "balance": build_variable_data(range_max=1000.0, mean=500.0, std=50.0),
                "income": build_variable_data(mean=20.0, std=3.0),
            }
        },
    }


def build_homogeneous_percentage_nodes_data(
    n: int, percentage: float
) -> dict[str, Any]:
    """A single-type population of ``n`` nodes all sharing one percentage rule.

    Useful for statistical tests on PercentageConnectivity: every node follows
    the same rule, so the whole matrix should reflect that one distribution.
    """
    return {
        "citizen": build_health_node_type_data(
            initial_numbers=n, percentage=percentage
        ),
    }


def build_nodes_data() -> dict[str, Any]:
    """A two-node-type population: 3 citizens + 2 companies (5 nodes total)."""
    return {
        "citizen": build_health_node_type_data(initial_numbers=3),
        "company": build_money_node_type_data(initial_numbers=2),
    }


def build_simulation_data(
    max_duration: int = 10,
    re_connection: bool = True,
    seed: int = 42,
    step_size: str = "1.0 months",
) -> dict[str, Any]:
    return {
        "max_duration": max_duration,
        "re_connection": re_connection,
        "seed": seed,
        "step_size": step_size,
    }


def build_blueprint_data() -> dict[str, Any]:
    """A complete blueprint dict with both 'nodes' and 'simulation' keys."""
    return {
        "nodes": build_nodes_data(),
        "simulation": build_simulation_data(),
    }


# ──────────────────────────────────────────────────────
# Concrete domain-object builders
# ──────────────────────────────────────────────────────
def build_health_module(
    health: float = 50.0, age: float = 30.0, **overrides: float
) -> HealthModule:
    """A HealthModule on the canonical HEALTH_PARAMS hazard parameters.

    Args:
        health: Seeded health; apply() overwrites it from age on the first step.
        age: Starting age.
        **overrides: Any HEALTH_PARAMS entry to replace for this module.

    Returns:
        The built HealthModule.
    """
    return HealthModule(health=health, age=age, **{**HEALTH_PARAMS, **overrides})


def build_node(
    node_id: int = 0,
    node_type: str = "citizen",
    modules: list | None = None,
) -> Node:
    if modules is None:
        modules = [build_health_module()]
    return Node(id=node_id, node_type=node_type, modules=modules)


def build_connectivity_matrix(data: NDArray | None = None) -> ConnectivityMatrix:
    if data is None:
        data = np.array([[0.0, 1.0], [1.0, 0.0]])
    return ConnectivityMatrix(data=data)


def build_simulation_specs(**overrides: Any) -> SimulationSpecs:
    """A SimulationSpecs wrapping the canonical simulation config dict."""
    return SimulationSpecs(build_simulation_data(**overrides))


def build_engine(
    nodes: list[Node] | None = None,
    connectivity_matrix: ConnectivityMatrix | None = None,
    simulation_specs: SimulationSpecs | None = None,
) -> SimulationEngine:
    """A SimulationEngine with a two-node population and 2x2 connectivity.

    The default population mixes a HealthModule node and a MoneyModule node so
    round-trip tests exercise more than one concrete module type.
    """
    if nodes is None:
        nodes = [
            Node(
                id=0,
                node_type="citizen",
                modules=[build_health_module(health=80.0, age=25.0)],
            ),
            Node(
                id=1,
                node_type="company",
                modules=[MoneyModule(balance=100.0, income=10.0)],
            ),
        ]
    if connectivity_matrix is None:
        connectivity_matrix = build_connectivity_matrix()
    if simulation_specs is None:
        simulation_specs = build_simulation_specs(max_duration=3)
    return SimulationEngine(
        nodes=nodes,
        connectivity_matrix=connectivity_matrix,
        simulation_specs=simulation_specs,
    )


def build_simulation(
    engine: SimulationEngine | None = None,
    history: list[SimulationState] | None = None,
    current_step: int = 0,
) -> SimulationRun:
    """A Simulation service object with a populated engine, history and step.

    The engine's step() is unimplemented, so history is injected directly
    (mirroring how the loader reconstructs a run) rather than produced by a run.
    """
    if engine is None:
        engine = build_engine()
    if history is None:
        state = SimulationState(
            nodes=engine.nodes,
            connectivity_matrix=engine.connectivity_matrix,
            time_idx=0,
            time_step=engine.simulation_specs.step_size,
        )
        history = [state]

    simulation = SimulationRun(engine=engine)
    simulation.current_step = current_step
    simulation.history = history
    return simulation
