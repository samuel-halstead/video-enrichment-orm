# Bump these on release
VERSION_MAJOR ?= 0
VERSION_MINOR ?= 1
VERSION_PATCH ?= 0
CHART_PATH ?= chart/

VERSION ?= $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_PATCH)

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: bumpversion
bumpversion:
	@poetry version $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_PATCH)
	@echo $(VERSION) > VERSION

.PHONY: name
name:
	@cat ${CHART_PATH}/Chart.yaml | grep name | cut -d " " -f 2

# Do quality checks
.PHONY: ruff
ruff:
	@poetry run ruff .

.PHONY: black
black:
	@poetry run black .

.PHONY: isort
isort:
	@poetry run isort .

.PHONY: typecheck
typecheck:
	@poetry run mypy video_enrichment_orm

# Do quality checks
.PHONY: quality
quality:
	poetry run black .
	poetry run isort . --profile black
	poetry run ruff --fix .

# Format code
.PHONY: format
format:
	@poetry run black .
	@poetry run isort . --profile black

.PHONY: pre-commit
pre-commit: format typecheck

# Do testing
.PHONY: unit_tests
unit_tests:
	@poetry run python -m pytest tests/unit --junitxml=junit-report-unit-tests.xml -o junit_suite_name="unit tests"

.PHONY: tests
tests:
	@poetry run python -m pytest tests --junitxml=junit-report-tests.xml -o junit_suite_name="tests"

# Alembic create new migration
create-migrations:
	poetry run alembic revision --autogenerate -m $(word 2, $(MAKECMDGOALS))

# Alembic run all pending migrations
run-migrations:
	poetry run alembic upgrade head

# Alembic list migrations
run-migrations-history:
	poetry run alembic history

# Alembic downgrade migration
run-downgrade-migration:
	poetry run alembic downgrade $(word 2, $(MAKECMDGOALS))

# Alembic downgrade migration to 0
run-downgrade-migration-base:
	poetry run alembic downgrade base
