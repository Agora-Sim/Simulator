"""Shared fixtures for the test suite.

Fixtures here are intentionally thin wrappers around the builders in
tests.helpers.builders, so tests can request common config shapes by name while
still being free to build bespoke data inline when needed.
"""

from __future__ import annotations

from typing import Any

import pytest

from tests.helpers import builders


@pytest.fixture
def nodes_data() -> dict[str, Any]:
    return builders.build_nodes_data()


@pytest.fixture
def simulation_data() -> dict[str, Any]:
    return builders.build_simulation_data()


@pytest.fixture
def blueprint_data() -> dict[str, Any]:
    return builders.build_blueprint_data()
