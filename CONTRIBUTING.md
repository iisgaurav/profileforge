# Contributing to ProfileForge

First off, thank you for considering contributing to ProfileForge!

ProfileForge is a community-driven open source project. To keep the engine robust, maintainable, and backward-compatible, all contributions follow our architectural layers and governance guidelines.

---

## 📖 Key Documentation

Before starting your contribution, please review:
- [Architecture Specification](file:///d:/WEB/profileforge/ARCHITECTURE.md) — Layer boundaries, dependency rules, and invariants.
- [Architecture Decision Records (ADRs)](file:///d:/WEB/profileforge/docs/adr/) — Key technical decisions.
- [RFC Process](file:///d:/WEB/profileforge/docs/RFC_PROCESS.md) — How to propose breaking changes or new layers.
- [Widget Authoring Guide](file:///d:/WEB/profileforge/docs/WIDGET_AUTHORING.md) — How to create new widgets.
- [Design System & Tokens](file:///d:/WEB/profileforge/docs/TOKENS.md) — Token definitions for theming.

---

## 🛠️ Development Setup

1. Clone the repository and navigate to the project directory.
2. Install with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Code formatting and linting:
   ```bash
   ruff format src/ tests/ tools/
   ruff check src/ tests/ tools/
   ```

4. Run the automated test suite:
   ```bash
   pytest
   ```

5. Verify API snapshot lock:
   ```bash
   python tools/api_lock.py --check
   ```

---

## 📋 Pull Request Guidelines

1. **Declare Layers**: When opening a PR, complete the **Layer Declaration Checklist** in the PR template.
2. **Respect Frozen Layers**: Core/Models, Themes, Components, Layout, and Render APIs cannot be broken without an approved [RFC](file:///d:/WEB/profileforge/docs/RFC_PROCESS.md).
3. **Verify API Lock**: Ensure `python tools/api_lock.py --check` passes cleanly in CI.
4. **Include Tests**: Add unit tests in `tests/` covering new features, edge cases, and bug fixes.
