.PHONY: format diagram lint typecheck dev coverage-badge install-hooks license license-check

license:
	poetry run python scripts/license_headers.py

license-check:
	poetry run python scripts/license_headers.py --check

diagram:
	classpy sync
	PLANTUML_LIMIT_SIZE=16384 plantuml -tpng docs/*.puml

format:
	docformatter --in-place --recursive --wrap-summaries 88 --wrap-descriptions 88 src/simulator
	black src/simulator/
	black tests/

lint:
	poetry run pylint --disable=C src/

# pyright ships as a node package; --pythonpath points it at the poetry venv
typecheck:
	npx --yes pyright@1.1.406 --pythonpath "$$(poetry env info --executable)"

dev: diagram license format lint typecheck

coverage-badge:
	poetry run python scripts/update_coverage_badge.py

install-hooks:
	cp .githooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
