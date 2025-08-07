.PHONY: help install install-dev lint format type-check test clean pre-commit

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

lint:  ## Run flake8 linter
	flake8 gui/ core/ plugins/ utils/ tests/

format:  ## Format code with black and isort
	black gui/ core/ plugins/ utils/ tests/
	isort gui/ core/ plugins/ utils/ tests/

type-check:  ## Run mypy type checker
	mypy gui/ core/ plugins/ utils/

test:  ## Run tests with pytest
	pytest tests/ -v

test-cov:  ## Run tests with coverage report
	pytest tests/ -v --cov --cov-report=html

clean:  ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files
