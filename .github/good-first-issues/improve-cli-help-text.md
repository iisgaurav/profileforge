# [Good First Issue] Make CLI Help Text More User-Friendly

## 🌟 Background

While `profileforge --help` is functionally complete, its output is currently brief and terse. We want to update CLI command help strings across Click / Typer decorators to be warm, clear, and rich with concrete usage examples so new developers can understand and use commands immediately.

## 🛠️ Commands to Improve

Enhance help docstrings and examples for these 6 CLI commands:

1. **`profileforge build`**
   - *Add examples*: `--config profileforge.yaml` and `--output ./dist`
2. **`profileforge new <name>`**
   - *Add examples*: `--template backend` or `--template minimalist`
3. **`profileforge validate`**
   - *Explain*: Details of config validation, connector verification, and schema checks.
4. **`profileforge doctor`**
   - *Explain*: Diagnostics suite checks (Python version >= 3.9, optional dependencies, environment keys).
5. **`profileforge widgets list`**
   - *Explain*: Description of tabular output format, categories, and status flags.
6. **`profileforge widgets info <id>`**
   - *Add example*: `profileforge widgets info github_stats` showing schema details.

## ✅ Acceptance Criteria

- [ ] Help text updated for all 6 target commands in CLI source modules
- [ ] Each command includes at least one concrete shell usage example in its `--help` string
- [ ] `profileforge --help` and all sub-command `--help` invocations display clear, nicely formatted output
- [ ] Zero functional logic or behavior changes
- [ ] All existing CLI tests continue to pass: `pytest tests/ -v`

## 💡 Code Reference

Look in `src/profileforge/cli/` modules where Click or Typer command definitions reside. Update docstrings and `help=` parameters.

---

- **Labels**: `good first issue`, `cli`, `ux`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 1–2 hours
