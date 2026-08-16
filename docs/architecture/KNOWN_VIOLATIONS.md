# Known Architectural Violations

This file documents Category B transitional architectural violations.
These are intentional, temporary deviations from the strict layered architecture (Widget -> Component -> Layout -> Renderer).

**Goal:** Zero entries before v1.0 public release.

Every architectural exception must be visible, documented here, and scheduled for removal.
Do not create silent whitelists in the 	ools/arch_check.py linter.

## Current Violations

*None currently.*

### Format for New Violations:
- **File**: path/to/file.py
- **Import**: rom profileforge.widgets import Something (inside Renderer)
- **Reason**: Migration to new layout engine in progress.
- **ADR/RFC**: docs/rfcs/003-layout.md
- **Owner**: @username
- **Removal Target Version**: v0.9.5
