# [Good First Issue] Design Spec for Drag-and-Drop Widget Reordering in Studio

## 🌟 Background

This is a **design specification issue** (RFC document—no implementation code required). As part of the upcoming Studio v2 milestone, we want to allow users to visually reorder their profile widgets using drag-and-drop within ProfileForge Studio (`web/index.html`).

We require a thorough, well-reasoned architectural proposal delivered as a markdown file at `docs/rfcs/studio-drag-drop.md`.

## 📄 Required Design Document Structure

Your proposal in `docs/rfcs/studio-drag-drop.md` must cover the following 5 sections in detail:

### 1. UX Flow
- How does the user initiate a drag interaction? (e.g. handle vs full card drag)
- Visual feedback state during active drag (opacity, box-shadow, drop indicator line).
- How the drop target zone highlights and confirms final position.

### 2. Data Model
- How widget order is tracked in memory.
- Concretely demonstrate the updated `profileforge.yaml` schema representing layout order.

### 3. Accessibility (A11y)
- Keyboard navigation alternative (e.g., Space to pick up, Up/Down arrow keys to move, Space to drop).
- ARIA live region announcements for screen readers (e.g. "Moved widget 'GitHub Stats' to position 2 of 5").

### 4. Implementation Approach
- Evaluate native HTML5 Drag and Drop API vs. lightweight zero-dependency JS (e.g., SortableJS via CDN or custom micro-script).
- Weigh pros and cons specifically for a serverless `file://` hosted single-page web app.

### 5. Edge Cases & Constraints
- Detailed matrix addressing edge cases (e.g. dragging between multi-column rows, grid span constraints, undo/redo state stack).

## ✅ Acceptance Criteria

- [ ] RFC document created at `docs/rfcs/studio-drag-drop.md`
- [ ] All 5 required sections covered thoroughly
- [ ] Includes at least one ASCII flow diagram depicting user interaction
- [ ] Accessibility section details specific keyboard keybindings and ARIA roles
- [ ] Concrete YAML snippet showing before/after `profileforge.yaml` schema modification
- [ ] Includes an edge cases table with at least 5 distinct failure/boundary scenarios

---

- **Labels**: `good first issue`, `studio`, `design`, `help wanted`
- **Difficulty**: ⭐ Easy (for UX / frontend designers)
- **Estimated Time**: 2–4 hours
