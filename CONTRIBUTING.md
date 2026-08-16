# Contributing to ProfileForge 🔥

Thank you for your interest in contributing to ProfileForge! Whether you're fixing a typo, adding a new theme, optimizing SVG rendering, or building a custom widget, every contribution makes the ecosystem richer for developers worldwide. This guide will help you set up your environment and walk you through our contribution workflow.

---

## 🗺️ Quick Navigation

| I want to... | Guide |
|---|---|
| Make my first open-source contribution | [FIRST_CONTRIBUTION.md](CONTRIBUTING.md) |
| Submit a new visual theme | [SUBMIT_THEME.md](docs/contributing/themes.md) |
| Submit a custom SVG widget | [SUBMIT_WIDGET.md](docs/contributing/widgets.md) |
| Submit a persona profile template | [SUBMIT_TEMPLATE.md](docs/contributing/templates.md) |
| Submit a data connector | [SUBMIT_CONNECTOR.md](docs/contributing/connectors.md) |
| Join the core team as a maintainer | [BECOME_MAINTAINER.md](CONTRIBUTING.md) |
| Understand the overall architecture | [ECOSYSTEM.md](ARCHITECTURE.md) |

---

## 🚀 Development Setup

To get started developing ProfileForge locally, follow these setup steps:

### 1. Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, or 3.13
- Git 2.25+
- Virtual environment tool (`venv` or `conda`)

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/iisgaurav/profileforge.git
cd profileforge

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Install package in editable mode with development dependencies
pip install -e ".[dev]"
```

### 3. Run Self-Diagnostics & Tests

Verify your setup by running the internal diagnostics tool and unit test suite:

```bash
# Run ProfileForge system doctor check
profileforge doctor

# Run full pytest test suite
pytest tests/ -v

# Run linter and formatter checks
ruff check .
ruff format --check .
```

---

## 🎯 Ways to Contribute & Difficulty Levels

We welcome contributions across all areas of the project! Here is a summary of contribution types and their typical difficulty:

| Contribution Type | Focus Area | Difficulty | Primary Skills |
|---|---|---|---|
| **Themes** | Visual styling & color palettes | ⭐ Easy | YAML, CSS Colors |
| **Templates** | Persona configs & scaffolds | ⭐ Easy | YAML, Scaffolding |
| **Documentation** | Guides, RFCs, & CLI help strings | ⭐ Easy | Markdown, Technical Writing |
| **Widgets** | New SVG visual components | ⭐⭐ Medium | Python, SVG XML |
| **Connectors** | Data fetching APIs & RSS | ⭐⭐ Medium | Python, REST APIs |
| **Layout Engine** | Two-pass sizing & grid arrangement | ⭐⭐⭐ Hard | Python, Geometry Math |
| **Core Architecture** | CLI, rendering pipeline, plugin system | ⭐⭐⭐ Hard | Python, System Design |

Looking for beginner-friendly tasks? Check out our curated list of **[Good First Issues](.github/good-first-issues/)**!

---

## 📦 Pull Request Guidelines

To maintain architectural integrity and high test quality, please ensure your Pull Request follows these guidelines:

### 1. Branch Naming & Layer Scoping
Name your branch clearly according to the task type:
- `feat/theme-tokyo-night`
- `fix/layout-row-wrap`
- `docs/widget-authoring-examples`

### 2. Architectural Rules & Layer Hierarchy
ProfileForge follows a strict layered architecture (`core` → `connectors` → `themes` → `layout` → `widgets` → `cli`).
- **Layer Declaration**: Note which architectural layer your changes affect in the PR description.
- **Frozen Layers**: Do not modify low-level core contracts (`src/profileforge/core/models.py`) without opening an RFC first.
- **API Lock Check**: Ensure no public function signatures are changed without updating dependent callers.

### 3. Code Standards & Linting
- Run `ruff check .` and fix all warnings.
- Format code using `ruff format .`.
- Add type annotations (`typing`) to all new Python functions.

### 4. Unit Testing Requirement
- Every new feature or bug fix must include corresponding tests in `tests/`.
- Ensure tests cover edge cases (e.g. empty data, missing API credentials).
- Run `pytest --cov=src/profileforge` to ensure coverage does not decrease.

---

## 🏛️ Project Architecture & Design System

Before submitting complex changes, take time to review our technical design docs:

- **High-Level Architecture**: Read [`ARCHITECTURE.md`](ARCHITECTURE.md) to understand rendering lifecycle, two-pass layout math, and caching pipelines.
- **Architectural Decision Records**: Browse [`docs/adr/`](docs/adr/) for historical design choices regarding SVG generation and YAML schema validation.
- **Ecosystem Overview**: Read [`ECOSYSTEM.md`](ARCHITECTURE.md) for details on plugins, connectors, and Studio web integrations.
- **Design & Visual Engineering**: Any PR modifying themes, layout, SVGs, or components MUST adhere to the 10 rules outlined in [`docs/DESIGN_ENGINEERING.md`](docs/DESIGN_ENGINEERING.md) and pass visual regression CI.

---

## 🎖️ Recognition & Community

Every contributor is valued!
- All merged code and documentation contributions are automatically acknowledged in [`CHANGELOG.md`](CHANGELOG.md).
- Significant contributors are invited to join the ProfileForge organization as maintainers (see [`BECOME_MAINTAINER.md`](CONTRIBUTING.md)).

---

## 📜 Code of Conduct

We are committed to fostering a welcoming, respectful, and inclusive community for everyone. All contributors and maintainers are expected to adhere to our Code of Conduct in all project spaces, issues, and pull requests. Be kind, collaborative, and constructive!

---

Thank you again for building ProfileForge with us! Happy coding! 🚀
