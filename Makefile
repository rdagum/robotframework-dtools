.PHONY: venv venv-check install-dev install clean-venv reset-env test lint format format-check safety venv-info help

help:
	@echo Available commands:
	@echo   venv        - Create virtual environment
	@echo   install-dev - Install development dependencies
	@echo   install     - Install production dependencies
	@echo   clean-venv  - Remove virtual environment
	@echo   reset-env   - Clean and recreate environment
	@echo   test        - Run tests
	@echo   lint        - Run linting
	@echo   format      - Format code with black
	@echo   format-check - Check code formatting with black
	@echo   safety      - Run safety check for vulnerabilities
	@echo   venv-info   - Show virtual environment information
	@echo   help        - Show this help

# Python and virtual environment settings
PYTHON := python
VENV := .venv
VENV_BIN := $(VENV)/Scripts
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# Check if virtual environment exists
venv-check:
	@if not exist "$(VENV)" ( \
		echo Virtual environment not found. Run 'make venv' first. && \
		exit /b 1 \
	)

# Create virtual environment
venv:
	@echo Creating virtual environment...
	$(PYTHON) -m venv $(VENV)
	@echo Virtual environment created in $(VENV)
	@echo Run 'make install-dev' to install dependencies

# Install development dependencies in virtual environment
install-dev: venv-check
	@echo Installing development dependencies...
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	@echo Development environment setup complete!

# Install production dependencies only
install: venv-check
	@echo Installing production dependencies...
	$(PIP) install .

# Clean virtual environment
clean-venv:
	@if exist "$(VENV)" ( \
		echo Removing virtual environment... && \
		rmdir /s /q "$(VENV)" \
	)

# Reset environment (clean and recreate)
reset-env: clean-venv venv install-dev

# Run tests in virtual environment
test: venv-check
	$(PYTHON_VENV) -m pytest --html=reports/report.html --self-contained-html

# Run tests with JUnit XML (for CI/CD)
test-ci: venv-check
	$(PYTHON_VENV) -m pytest --junit-xml=reports/junit.xml

# Run tests with coverage report
test-coverage: venv-check
	$(PYTHON_VENV) -m pytest --cov=. --cov-report=html:htmlcov --cov-report=term

# Run linting in virtual environment  
lint: venv-check
	$(PYTHON_VENV) -m flake8

# Format code with black
format: venv-check
	@echo Formatting code with black...
	$(PYTHON_VENV) -m black .
	@echo Code formatting complete!

# Check code formatting with black
format-check: venv-check
	@echo Checking code formatting with black...
	$(PYTHON_VENV) -m black --check --diff .

# Run safety check for vulnerabilities
safety: venv-check
	@echo Running safety scan for vulnerabilities...
	$(PYTHON_VENV) -m safety scan

# Show virtual environment info
venv-info:
	@if exist "$(VENV)" ( \
		echo Virtual environment: $(VENV) && \
		echo Python: $(PYTHON_VENV) && \
		echo Pip: $(PIP) \
	) else ( \
		echo No virtual environment found. Run 'make venv' to create one. \
	)