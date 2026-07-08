#!/usr/bin/env python3
"""Run the test suite under coverage and refresh the coverage badge in README.md."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

BADGE_START = "<!-- coverage-badge:start -->"
BADGE_END = "<!-- coverage-badge:end -->"


def _color_for(pct: int) -> str:
    if pct >= 90:
        return "brightgreen"
    if pct >= 75:
        return "green"
    if pct >= 50:
        return "yellow"
    return "red"


def _run_coverage() -> int:
    subprocess.run(
        ["coverage", "run", "-m", "pytest"],
        cwd=ROOT,
        check=True,
    )
    result = subprocess.run(
        ["coverage", "report", "--format=total"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def _badge_markdown(pct: int) -> str:
    color = _color_for(pct)
    url = f"https://shields.io/badge/coverage-{pct}%25-{color}?style=flat"
    return f'{BADGE_START}\n    <img src="{url}" alt="Coverage">\n    {BADGE_END}'


def _update_readme(pct: int) -> bool:
    text = README.read_text()
    badge = _badge_markdown(pct)
    pattern = re.compile(
        re.escape(BADGE_START) + r".*?" + re.escape(BADGE_END), re.DOTALL
    )

    if pattern.search(text):
        new_text = pattern.sub(badge, text)
    else:
        anchor = '<img src="https://shields.io/badge/linting-pylint-yellow?&style=flat" alt="Linter">'
        if anchor not in text:
            print("Could not find badge anchor in README.md; badge not inserted.")
            return False
        new_text = text.replace(anchor, f"{anchor}\n    {badge}")

    if new_text == text:
        return False

    README.write_text(new_text)
    return True


def main() -> int:
    pct = _run_coverage()
    changed = _update_readme(pct)
    print(f"Coverage: {pct}%" + (" (README updated)" if changed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
