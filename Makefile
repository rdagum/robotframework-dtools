.PHONY: help install install-dev test test-unit test-robot lint format type-check clean build docs

help:
	@echo "Available commands:"
	@echo "  install     Install the package"
	@echo "  install-dev Install development dependencies"
	@echo "  test        Run all tests"
	@echo "  test-unit   Run Python unit tests"
	@echo "  test-robot  Run Robot Framework tests"
	@echo "  lint        Run code linting"
	@echo "  format      Format code with Black"
	@echo "  type-check  Run type checking with MyPy"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build distribution packages"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test: test-unit test-robot

test-unit:
	pytest tests/test_dtools.py -v --cov=dtools --cov-report=html

test-robot:
	robot tests/test_dtools.robot

lint:
	flake8 dtools/

format:
	black dtools/ tests/

type-check:
	mypy dtools/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f output.xml log.html report.html

build:
	python -m build