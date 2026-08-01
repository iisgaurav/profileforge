# [Good First Issue] Increase Layout Engine Test Coverage

## 🌟 Background

The ProfileForge layout engine (`src/profileforge/layout/`) is responsible for calculating bounding dimensions, managing two-pass layout constraints, and arranging widgets in grids, rows, columns, and Bento layouts. Increasing unit test coverage across boundary conditions ensures structural stability across all theme layouts.

## 🧪 Wanted Test Scenarios

Add unit test functions in `tests/test_layout.py` covering the following scenarios:

1. **Bento grid with odd number of widgets**: Verify that an odd count of widgets fills space gracefully without overlapping or throwing index out-of-range errors.
2. **Row wrapping**: When total width of children exceeds container bounds, verify that wrapping calculates line breaks and height correctly.
3. **Nested Column inside Row**: Verify fixed-width child placement alongside flex-fill children within a nested container hierarchy.
4. **Empty children containers**: Ensure `Column`, `Row`, and `Wrap` components with 0 children render smoothly without zero-division or null errors.
5. **Single child layout**: Verify grid and flex behavior when given exactly one widget element.

## ✅ Acceptance Criteria

- [ ] At least 4 new unit test functions added to `tests/test_layout.py`
- [ ] Each test function includes a descriptive docstring explaining the tested boundary condition
- [ ] All new tests pass when executing `pytest tests/test_layout.py -v`
- [ ] Existing layout test suite passes cleanly with no regressions
- [ ] Test coverage for `src/profileforge/layout/` increases measurable percentage (verify with `pytest --cov=src/profileforge/layout`)

## 💡 Testing Commands

```bash
# Run layout test suite
pytest tests/test_layout.py -v

# Measure coverage
pytest --cov=src/profileforge/layout tests/test_layout.py
```

---

- **Labels**: `good first issue`, `testing`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 2–3 hours
