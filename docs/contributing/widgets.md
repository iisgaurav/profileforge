# Submit a Widget

Thank you for building a new widget for ProfileForge! Widgets are the core building blocks of a ProfileForge profile.

This guide provides the checklist for submitting a widget. Before starting, please thoroughly read [WIDGET_AUTHORING.md](../WIDGET_AUTHORING.md) for technical instructions on how to write widgets.

## Overview

Widgets in ProfileForge are Python classes that follow a strict 6-phase lifecycle (Init, Fetch, Process, Layout, Render, Error/Fallback). All custom widgets must be robust, safe, and style-agnostic (relying on themes).

## Pre-Submission Checklist

Please ensure your widget meets all of the following requirements before submitting a PR:

- [ ] **Metadata**: The widget class has full metadata defined (name, description, version, author).
- [ ] **Lifecycle**: Implements all 6 lifecycle phases correctly.
- [ ] **Safe Rendering**: `render_safe()` is implemented and tested to prevent template injection.
- [ ] **No Hardcoded Styles**: Uses `var(--color-primary)`, `var(--radius-md)`, etc. instead of raw hex or px values.
- [ ] **Design Tokens**: Fully utilizes the ProfileForge design token system.
- [ ] **Unit Tests**: comprehensive unit tests in `tests/widgets/` (mocking connectors and testing outputs).
- [ ] **Docstrings**: The class and all public methods have clear Python docstrings.
- [ ] **Fallback Tested**: The widget degrades gracefully if data fetching fails or times out.
- [ ] **Connector Declared**: Dependencies on data connectors are explicitly declared.
- [ ] **Experimental Flag**: If the widget uses unstable APIs, it is marked with the `is_experimental=True` flag.
- [ ] **File Location**: The widget is placed in `src/profileforge/widgets/`.
- [ ] **Registration**: The widget class is decorated with `@register_widget(name="your_widget_name")`.

## Test Commands

Run the following before opening your PR:

```bash
# Validate your specific widget
profileforge validate --widget your_widget_name

# Run the test suite
pytest tests/widgets/test_your_widget.py -v

# Check types and style
ruff check src/profileforge/widgets/your_widget.py
```

## Pull Request Description

When submitting, please use the following structure in your PR description:

```markdown
### What does this widget do?
[Explain the purpose and visual output of the widget]

### Screenshot / SVG Output
[Attach a preview of the rendered SVG widget]

### Connectors Used
[List data connectors required, e.g., GitHub GraphQL API]

### Checklist Completed?
[Confirm you've read and checked the items above]
```

## What Makes a Widget Merge-Ready?

A merge-ready widget is visually polished, uses the theme system properly so it looks good on both Light and Dark themes, handles API rate limits elegantly via its connector, and has 100% test coverage for its data processing logic.
