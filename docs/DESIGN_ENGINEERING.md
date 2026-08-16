# Design System Engineering Rules

This document serves as the single source of truth for all ProfileForge visual, design, and rendering engineering standards. It dictates how widgets are authored, how the architecture is maintained, and how visual QA is enforced.

## 1. Philosophy

ProfileForge is **architecture-first**, **design-system driven**, **extensible**, **production-ready**, **deterministic**, and **framework-based**.
Optimize for craftsmanship, consistency, and long-term maintainability—not just shipping features.

**Never stop at "looks better".** Every visual change must be justified, deterministic, and rigorously regression-tested.

## 2. Design Hierarchy

Never fix an individual widget first. Always ask:
*"Is this a renderer problem, a layout problem, a component problem, a theme problem, or a widget problem?"*

Fix issues at the lowest reusable layer possible.
**Priority Stack:**
1. Theme (Tokens)
2. Renderer
3. Layout Engine
4. Component
5. Widget

Widgets should almost never contain visual hacks.

## 3. Design Tokens

**Every spacing value must come from tokens.**
Never introduce magic values like `17`, `21`, `37`, `53`.
Every spacing value must come from the design token system. If a token doesn't exist, propose adding one rather than hardcoding numbers.

## 4. Visual QA Process

Visual QA is divided into two independent systems:

### Objective QA (Automated)
Fails CI if criteria are unmet:
* SVG is valid XML
* No clipping or overflow
* No text outside bounds
* No missing icons
* No duplicate IDs
* Theme tokens properly resolved
* Accessibility tags present
* Generated PNG matches expected dimensions
* No renderer exceptions

### Design Review (Human / Vision)
Aesthetic review must remain qualitative. Reviewers examine:
* Alignment
* Padding
* Typography
* Hierarchy
* Visual Balance
* Consistency

## 5. Regression Workflow

Every visual change must improve the whole ecosystem. Never optimize only one widget.
After changing the renderer or layout engine:
1. Regenerate every SVG.
2. Render every PNG.
3. Inspect the entire gallery.
4. Ensure nothing regressed.

**CI Behaviour:** CI will not fail simply because pixels changed (to allow intentional redesigns).
Instead:
`Visual Difference Detected` → `Generate artifacts` → `Require DESIGN_QA.md` → `Reviewer approves` → `Merge`.

## 6. PR Requirements

Every UI-related PR must include:
* `before.png` / `before.svg`
* `after.png` / `after.svg`
* A completed `DESIGN_QA.md` report answering:
    * Problem & Root Cause
    * Architectural Layer
    * Changes
    * Visual Before / After
    * Regression Risk & Remaining Issues

## 7. Common Anti-patterns

* **Hardcoded Dimensions**: Bypassing layout engine constraints.
* **Competitor Copying**: Study products like Linear, Vercel, Stripe, GitHub, Raycast, Arc, Apple Developer to understand *why* they look good. Do not copy them. ProfileForge develops its own recognizable design language.
* **Blind Implementation**: If you believe a requested visual change hurts consistency, explain why and propose a better alternative. Protect the integrity of the design system.

## 8. Visual Regression Gallery

A canonical gallery of baseline artifacts is maintained at `gallery/`:
* `gallery/before/`
* `gallery/after/`
* `gallery/diff/`
* `gallery/reports/`

Every visual PR must update this gallery.

## 9. Checklist

See the Pull Request Template for the mandatory Layer Declaration and Visual Checklist.

## 10. Release Blocking Policy

Layers 1–5 remain frozen. Breaking changes to these layers require:
* RFC
* ADR
* Major version bump

No exceptions. Every architectural exception (Category B transitional violations) must be visible, documented in `docs/architecture/KNOWN_VIOLATIONS.md`, and scheduled for removal. Never create a silent whitelist.
