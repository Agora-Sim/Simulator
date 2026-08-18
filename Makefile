.PHONY: format diagram lint dev coverage-badge install-hooks license license-check

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

dev: diagram license format lint

coverage-badge:
	poetry run python scripts/update_coverage_badge.py

install-hooks:
	cp .githooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
