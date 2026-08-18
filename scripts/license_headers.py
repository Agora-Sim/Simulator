# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 GuilhermeCF

"""SPDX license header maintenance for the Python sources.

The project ships under AGPL-3.0-or-later (see pyproject.toml and LICENSE), so
every .py file carries a two-line SPDX header as its first lines. This script
is the single source of truth for that header: it can report which files are
missing it (`--check`, used by the test suite and the pre-commit hook) or
insert it in place (default).
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
from __future__ import annotations

import sys
from pathlib import Path

# ================================================================
# 1. Section: CONSTANTS
# ================================================================
SPDX_TAG = "SPDX-License-Identifier: AGPL-3.0-or-later"
COPYRIGHT = "Copyright (C) 2026 GuilhermeCF"
HEADER = f"# {SPDX_TAG}\n# {COPYRIGHT}\n"

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FOLDERS = ("src", "tests", "scripts")


# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def python_files() -> list[Path]:
    """Return every tracked .py file the header applies to, sorted by path."""
    files: list[Path] = []
    for folder in SOURCE_FOLDERS:
        files.extend((REPO_ROOT / folder).rglob("*.py"))
    return sorted(f for f in files if "__pycache__" not in f.parts)


def has_header(path: Path) -> bool:
    """Return whether the file already declares the SPDX identifier."""
    return SPDX_TAG in path.read_text(encoding="utf-8")[:512]


def missing_header() -> list[Path]:
    """Return the files that lack the SPDX header."""
    return [f for f in python_files() if not has_header(f)]


def add_header(path: Path) -> None:
    """Prepend the header, keeping a shebang line first when present."""
    text = path.read_text(encoding="utf-8")
    # an empty __init__.py gets the header alone, with no trailing blank line
    if not text.strip():
        path.write_text(HEADER, encoding="utf-8")
        return
    if text.startswith("#!"):
        shebang, _, rest = text.partition("\n")
        path.write_text(f"{shebang}\n{HEADER}\n{rest}", encoding="utf-8")
        return
    path.write_text(f"{HEADER}\n{text}", encoding="utf-8")


def main(argv: list[str]) -> int:
    """Run in check mode (`--check`) or insert the missing headers."""
    pending = missing_header()
    if "--check" in argv:
        for path in pending:
            print(f"missing SPDX header: {path.relative_to(REPO_ROOT)}")
        return 1 if pending else 0
    for path in pending:
        add_header(path)
        print(f"added SPDX header: {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
