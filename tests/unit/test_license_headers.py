# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

"""Repo-wide guard for the SPDX license headers.

The project is AGPL-3.0-or-later, so every .py file under src/, tests/ and
scripts/ must open with the SPDX header. `make license` inserts it; this test
is what makes a forgotten header fail loudly instead of drifting in silently.
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# scripts/ is not an installed package, so it is imported by path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import license_headers  # pylint: disable=wrong-import-position


# ================================================================
# 1. Section: TESTS
# ================================================================
@pytest.mark.unit
def test_every_python_file_has_the_spdx_header():
    """No source, test or script file may be missing the SPDX header."""
    pending = [
        str(p.relative_to(license_headers.REPO_ROOT))
        for p in license_headers.missing_header()
    ]
    assert not pending, f"run `make license` for: {pending}"


@pytest.mark.unit
def test_the_file_list_is_not_empty():
    """Guard the collector itself: an empty sweep would pass vacuously."""
    assert len(license_headers.python_files()) > 100


@pytest.mark.unit
def test_add_header_preserves_a_shebang(tmp_path):
    """The header goes below a shebang so the file stays executable."""
    script = tmp_path / "tool.py"
    script.write_text("#!/usr/bin/env python\nprint(1)\n", encoding="utf-8")

    license_headers.add_header(script)

    lines = script.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "#!/usr/bin/env python"
    assert license_headers.SPDX_TAG in lines[1]


@pytest.mark.unit
def test_add_header_keeps_existing_content(tmp_path):
    """Inserting the header must not drop or reorder the module body."""
    module = tmp_path / "mod.py"
    module.write_text('"""Doc."""\n\nVALUE = 1\n', encoding="utf-8")

    license_headers.add_header(module)

    text = module.read_text(encoding="utf-8")
    assert text.startswith(license_headers.HEADER)
    assert text.endswith('"""Doc."""\n\nVALUE = 1\n')
    assert license_headers.has_header(module)


@pytest.mark.unit
def test_has_header_is_false_for_a_bare_file(tmp_path):
    """A file without the tag is reported as missing."""
    module = tmp_path / "bare.py"
    module.write_text("VALUE = 1\n", encoding="utf-8")

    assert not license_headers.has_header(module)
