# Variables
PYTHON = python3
PIP = pip

.PHONY: install run debug clean lint lint-strict

install:
	$(PIP) install --upgrade pip build
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -r {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict