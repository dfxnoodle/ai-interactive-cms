# AI Interactive CMS - Makefile
# Use uv for Python package management

.PHONY: help install dev run clean test format lint serve-html

# Default target
help:
	@echo "AI Interactive CMS - Available commands:"
	@echo ""
	@echo "  install     Install dependencies using uv"
	@echo "  dev         Install with development dependencies"
	@echo "  run         Start the FastAPI server"
	@echo "  clean       Clean up virtual environment and cache"
	@echo "  test        Run tests (requires pytest)"
	@echo "  format      Format code with black and isort"
	@echo "  lint        Check code quality with flake8"
	@echo "  sync        Sync dependencies from pyproject.toml"
	@echo "  serve-html  Start auto-reload development server for HTML files"
	@echo ""
	@echo "Quick start: make install && make run"

# Install dependencies
install:
	uv venv
	uv pip install -r requirements.txt

# Install with development dependencies
dev:
	uv sync --dev

# Sync dependencies from pyproject.toml
sync:
	uv sync

# Run the application
run:
	uv run python main.py

# Start with auto-reload for development
dev-run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Clean up
clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete

# Run tests
test:
	uv run pytest

# Format code
format:
	uv run black .
	uv run isort .

# Check code quality
lint:
	uv run flake8 .

# Serve HTML files with auto-reload (for sample-html development)
serve-html:
	@echo "🚀 Starting auto-reload server for HTML development..."
	@echo "📁 Serving files from sample-html/ directory"
	@echo "🌐 Open http://localhost:8080 in your browser"
	@echo "🔄 Files will auto-refresh when you save changes"
	@echo "⏹️  Press Ctrl+C to stop"
	uv run python dev_server.py sample-html 8080

# Install uv if not present
install-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}

# Complete setup for new users
setup: install-uv sync
	@echo "Setup complete! Run 'make run' to start the server."
