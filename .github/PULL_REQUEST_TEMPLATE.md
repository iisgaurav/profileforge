## Summary & Context

<!-- Provide a concise explanation of what this pull request changes and why. -->

---

## 🏛️ Layer Declaration Checklist (Mandatory)

According to the ProfileForge Architecture Specification (`ARCHITECTURE.md`), every PR must declare which architectural layer(s) it touches:

- [ ] **Layer 1: Core / Models** (`profileforge.core`)
- [ ] **Layer 2: Themes** (`profileforge.themes`, token definitions)
- [ ] **Layer 3: Components** (`profileforge.components`)
- [ ] **Layer 4: Layout** (`profileforge.render.layout`)
- [ ] **Layer 5: Render / SVG** (`profileforge.render`)
- [ ] **Layer 6: Connectors** (`profileforge.connectors`)
- [ ] **Layer 7: Widgets** (`profileforge.widgets`)
- [ ] **Layer 8: CLI / Application Orchestration** (`profileforge.cli`)
- [ ] **Documentation & Tooling** (`docs/`, `tools/`, `.github/`)

---

## 🏷️ Type of Change

- [ ] 🐛 **Bug fix** (non-breaking change fixing an issue)
- [ ] ✨ **New feature** (non-breaking change adding functionality)
- [ ] 🎨 **New Theme / Widget** (community contribution adhering to standard interfaces)
- [ ] ⚠️ **Breaking Change / RFC** (modifies frozen Layer 1-5 APIs; requires approved RFC)
- [ ] ⚡ **Performance improvement**
- [ ] ♻️ **Refactoring / Code quality**
- [ ] 📚 **Documentation update**

---

## ⚠️ Breaking Changes & RFC Governance

Does this PR introduce breaking changes or modify frozen layer APIs?
- [ ] **No** — This PR strictly preserves existing public symbols and method signatures.
- [ ] **Yes** — This PR contains breaking changes.
  - **Approved RFC Link**: `docs/rfcs/YYYY-MM-DD-feature.md` or PR #
  - **API Snapshot Updated**: `python tools/api_lock.py --update` executed and committed.

---

## ✅ Quality & Verification Checklist

Before submitting, please ensure the following pass locally:

- [ ] Linting passes: `ruff check src/ tests/ tools/`
- [ ] Formatting passes: `ruff format --check src/ tests/ tools/`
- [ ] Test suite passes: `pytest`
- [ ] API Snapshot Lock passes: `python tools/api_lock.py --check`
- [ ] New unit tests added for new features or bug fixes
- [ ] Documentation updated in `docs/` where applicable
