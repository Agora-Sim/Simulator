"""Builders for domain test data.

These helpers produce the raw config dictionaries the domain instantiation
layer consumes, plus convenience builders for concrete domain objects. Keeping
the canonical shapes in one place means a change to the config schema only has
to be reflected here, not in every test.
"""

from __future__ import annotations

from typing import Any

from simulator.domain.node import Node
from simulator.domain.modules import HealthModule, MoneyModule


# ──────────────────────────────────────────────────────
# Raw config-dict builders (what the user file would contain)
# ──────────────────────────────────────────────────────
def build_normal_connectivity_data(
    mean: float = 2.0, std: float = 1.0
) -> dict[str, Any]:
    return {"type": "normal", "mean": mean, "std": std}


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
    initial_numbers: int = 3,
    mean: float = 2.0,
    std: float = 1.0,
) -> dict[str, Any]:
    return {
        "initial_numbers": initial_numbers,
        "connectivity": build_normal_connectivity_data(mean=mean, std=std),
        "modules": {
            "health_module": {
                "health": build_variable_data(mean=50.0, std=5.0),
                "age": build_variable_data(mean=30.0, std=2.0),
            }
        },
    }


def build_money_node_type_data(initial_numbers: int = 2) -> dict[str, Any]:
    return {
        "initial_numbers": initial_numbers,
        "connectivity": build_normal_connectivity_data(mean=1.0, std=0.5),
        "modules": {
            "money_module": {
                "balance": build_variable_data(range_max=1000.0, mean=500.0, std=50.0),
                "income": build_variable_data(mean=20.0, std=3.0),
            }
        },
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
def build_node(
    node_id: int = 0,
    node_type: str = "citizen",
    modules: list | None = None,
) -> Node:
    if modules is None:
        modules = [HealthModule(health=50.0, age=30.0)]
    return Node(id=node_id, node_type=node_type, modules=modules)
