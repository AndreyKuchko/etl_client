PYTHON            := .venv/bin/python
PIP               := .venv/bin/pip
PYTHON_BLACK      := .venv/bin/python -m black --line-length 100
PYTHON_MYPY       := .venv/bin/mypy --python-executable .venv/bin/python
PYTHON_PYTEST     := .venv/bin/pytest -vvv

PYTHON_PATH       ?= $(shell which python3)


.PHONY: clean
clean::
	rm -fR .venv .mypy_cache .pytest_cache tests/.pytest_cache build build_deps sdist *.egg-info

.PHONY: clean_output
clean_output::
	rm -fR output/*.csv

.venv:
	$(PYTHON_PATH) -m venv --clear .venv && $(PIP) install --upgrade pip

.PHONY: install
install: .venv
	$(PIP) install -U -e .

.PHONY: black_validation
black_validation:
	$(PYTHON_BLACK) --check . \
	|| ( $(PYTHON_BLACK) --diff . && exit 1 )

.PHONY: mypy_validation
mypy_validation:
	$(PYTHON_MYPY) .

.PHONY: validate_files
validate_files: mypy_validation black_validation

.PHONY: test_install
test_install: install
	$(PIP) install -U -e ."[testing]"

.PHONY: unit_test
unit_test: test_install
	$(PYTHON_PYTEST) tests

.PHONY: test
test: test_install
	@make validate_files
	@make unit_test
