# Contributing to Simulator

Thanks for your interest in contributing. This document covers the CLA requirement and the basic workflow for getting a change merged.

## Contributor License Agreement (CLA)

Before we can merge your first contribution, you need to sign AgoraSim's Contributor License Agreement. This applies to all AgoraSim projects, not just this one: sign once and you're covered everywhere under the [Agora-Sim](https://github.com/Agora-Sim) organization.

1. Read the agreement: [Agora-Sim/cla-signatures/CLA.md](https://github.com/Agora-Sim/cla-signatures/blob/main/CLA.md)
2. Open a pull request against [Agora-Sim/cla-signatures](https://github.com/Agora-Sim/cla-signatures) that adds a file at `signatures/<your-github-username>.md` containing the line:

   ```
   I sign the Contributor License Agreement as it is currently written in CLA.md.
   ```

3. Once that PR is merged, you're set. No further action needed for this or any future AgoraSim contribution.

You can sign before or alongside your first PR to this repo; just make sure it's merged before we merge your code.

## Development setup

```bash
poetry install
```

Requires Python 3.13 (`>=3.13, <3.14`). See [pyproject.toml](pyproject.toml) for the full dependency list.

## Before opening a PR

```bash
make dev                                # diagram + format + lint
poetry run pytest -m "not slow" -q      # tests (pre-push default)
```

Always use `poetry run`: this project's dependencies (numpy, h5py, ...) only exist inside the poetry virtualenv.

## Code style

This repo follows a specific set of conventions: architecture layering (Service / Domain / Adapter), comment discipline, docstring templates, and file banner structure. Read [CLAUDE.md](CLAUDE.md) before making non-trivial changes; it's the source of truth for how code here is structured and reviewed.

## Opening a pull request

Use the repo's [PR template](.github/pull_request_template.md): describe what the change does and why, and how to use any new feature. Link the issue it closes if there is one.

## License

By contributing, you agree your contribution is licensed under this project's license, [AGPL-3.0-or-later](LICENSE), per the terms of the CLA above.
