# Contributing to ProfileForge

First off, thank you for considering contributing to ProfileForge!

## Development Setup

1. Clone the repo.
2. Install with development dependencies:
```bash
pip install -e ".[dev]"
```

3. We use `black` for formatting and `ruff` for linting.
```bash
black src/ tests/
ruff check src/ tests/
```

4. Run tests before submitting a PR:
```bash
pytest tests/
```
