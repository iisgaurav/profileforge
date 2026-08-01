# [Good First Issue] Add Python 3.13 to CI Matrix

## 🌟 Background

Python 3.13 has been officially released. ProfileForge targets Python 3.9+ and must verify that the full build pipeline and test suite pass cleanly on Python 3.13.

## 📝 Required Changes

1. Update `.github/workflows/ci.yml` build matrix to include Python `3.13`.
2. Verify `pyproject.toml` `requires-python` specification covers Python 3.13 (e.g. `>=3.9`).
3. Ensure no deprecated standard library modules (like `distutils`, removed in Python 3.12/3.13) cause import errors.

## ✅ Acceptance Criteria

- [ ] `.github/workflows/ci.yml` workflow matrix updated to:
  ```yaml
  python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
  ```
- [ ] All unit and integration tests pass on Python 3.13 without code modifications
- [ ] `pyproject.toml` configuration verified
- [ ] Any deprecation warnings specific to Python 3.13 noted in the PR description
- [ ] GitHub Actions build status matrix shows green across all 5 Python versions

## 💡 Technical Notes

- Note that `distutils` was removed in Python 3.12+. Confirm ProfileForge relies solely on `setuptools` or standard library `importlib`.
- Test locally if you have Python 3.13 installed:
  ```bash
  python3.13 -m pytest tests/ -v
  ```

---

- **Labels**: `good first issue`, `ci`, `infrastructure`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 1–2 hours
