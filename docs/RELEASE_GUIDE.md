# ProfileForge Release Engineering Guide

This guide establishes the standard operating procedure for preparing, validating, and publishing official releases of **ProfileForge**.

---

## 1. Versioning Policy (Semantic Versioning 2.0.0)

ProfileForge strictly adheres to [Semantic Versioning (SemVer 2.0.0)](https://semver.org/):

$$\text{MAJOR}.\text{MINOR}.\text{PATCH}$$

- **MAJOR ($X.0.0$)**: Incompatible API breaking changes. Any breaking change to `profileforge.core`, `profileforge.components`, `profileforge.widgets`, or `profileforge.render` requires an approved RFC (see `docs/RFC_PROCESS.md`) and a MAJOR version bump.
- **MINOR ($x.Y.0$)**: Backwards-compatible new features, new official widgets, new themes, new template personas, or new CLI commands.
- **PATCH ($x.y.Z$)**: Backwards-compatible bug fixes, performance optimizations, documentation updates, and internal refactors.

---

## 2. Release Gates & Automated Verification

No release may be tagged or published without passing all **6 Pre-Flight Quality Gates**:

```bash
python tools/release.py check
```

The release tool automatically validates:
1. **SemVer Synchronization**: Ensures `pyproject.toml` and `src/profileforge/__init__.py` versions match identically.
2. **Unit & Integration Test Suite**: Complete test suite execution via `pytest`.
3. **Code Linting & Formatting**: Strict style enforcement via `ruff check .`.
4. **Public API Lock Snapshot**: Signature drift validation via `python tools/api_lock.py --check`.
5. **Performance Budget Gate**: Sub-50ms SLA validation via `python tools/performance_check.py`.
6. **ADR Index & Consistency**: Architecture record validation via `python tools/adr_index.py --check`.
7. **Documentation QA**: Markdown YAML code blocks, CLI citations, and internal link validation via `tools/docs_check.py`.

---

## 3. Step-by-Step Release Workflow

### Step 1: Prepare Release Branch
```bash
git checkout main
git pull origin main
git checkout -b release/v1.0.0
```

### Step 2: Bump Version
```bash
# For patch release:
python tools/release.py bump patch

# For minor release:
python tools/release.py bump minor

# For major release:
python tools/release.py bump major
```

### Step 3: Generate Changelog & Release Notes
```bash
python tools/release.py changelog --version 1.0.0
```
Review and edit `CHANGELOG.md` to ensure all key community contributions and features are highlighted.

### Step 4: Execute Full Pre-Flight Gate
```bash
python tools/release.py check
```
Verify that all 6 quality gates display `[PASS]`.

### Step 5: Commit & Push Release Branch
```bash
git add pyproject.toml src/profileforge/__init__.py CHANGELOG.md
git commit -m "chore(release): prepare v1.0.0"
git push origin release/v1.0.0
```
Open and merge PR into `main`.

### Step 6: Tag the Release
```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Step 7: Build & Publish Distribution Artifacts
```bash
# Install build tools
pip install build twine

# Build source distribution and wheel
python -m build

# Check distribution integrity
twine check dist/*

# Upload to PyPI (automated via GitHub Actions on tag push)
twine upload dist/*
```

---

## 4. Hotfix & Emergency Patch Procedure

In the event of a critical regression on a published release:
1. Branch from the release tag: `git checkout -b hotfix/v1.0.1 v1.0.0`
2. Apply minimal targeted fix with dedicated regression test.
3. Bump patch version: `python tools/release.py bump patch`
4. Run full pre-flight verification: `python tools/release.py check`
5. Tag and publish `v1.0.1`.
6. Backport the fix to `main`.
