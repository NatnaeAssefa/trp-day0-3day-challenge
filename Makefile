# Project Chimera — standardised commands (Challenge Task 3.2)
# Use: make setup | make test | make spec-check

.PHONY: setup test spec-check lint

setup:
	uv sync || pip install -e .

test:
	docker build -t chimera . && docker run --rm chimera

spec-check:
	@echo "Checking specs/ presence and key files..."
	@test -f specs/_meta.md && test -f specs/functional.md && test -f specs/technical.md && echo "specs/ OK" || (echo "spec-check: missing spec files" && exit 1)

lint:
	ruff check src tests
	ruff format --check src tests
