.PHONY: format diagram dev coverage-badge install-hooks

diagram:
	plantuml -tpng docs/class.puml

format:
	docformatter --in-place --recursive --wrap-summaries 88 --wrap-descriptions 88 src/simulator
	black src/simulator/
	black test/

dev: diagram format

coverage-badge:
	poetry run python scripts/update_coverage_badge.py

install-hooks:
	cp .githooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
